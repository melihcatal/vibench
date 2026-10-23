from security_client import SecurityClients
from datetime import datetime
from typing import List, Dict
import json

class KeyUsageSummary:
    def __init__(self, key_id: str, event_name: str, event_time: datetime, username: str, source_ip: str):
        self.key_id = key_id
        self.event_name = event_name
        self.event_time = event_time
        self.username = username
        self.source_ip = source_ip

def summarize_kms_key_usage(
    key_id_filter: str,
    start_time: datetime,
    end_time: datetime,
    event_names: List[str] = None
) -> List[KeyUsageSummary]:
    cloudtrail_client = SecurityClients.get_aws_cloudtrail_client()

    if event_names is None:
        # Common AWS KMS event names to look for
        event_names = [
            "Encrypt", "Decrypt", "GenerateDataKey", "ReEncrypt", "Sign", "Verify",
            "CreateKey", "ScheduleKeyDeletion", "CancelKeyDeletion", "EnableKey", "DisableKey"
        ]

    summaries: List[KeyUsageSummary] = []
    
    next_token = None
    while True:
        try:
            kwargs = {
                'LookupAttributes': [
                    {'AttributeKey': 'EventName', 'AttributeValue': name} for name in event_names
                ],
                'StartTime': start_time,
                'EndTime': end_time,
            }
            if next_token:
                kwargs['NextToken'] = next_token

            response = cloudtrail_client.lookup_events(**kwargs)

            for event in response.get('Events', []):
                cloudtrail_event_json = event.get('CloudTrailEvent')
                if cloudtrail_event_json:
                    event_data = json.loads(cloudtrail_event_json)
                    
                    used_key_id = None
                    # Look for KeyId in requestParameters
                    if 'requestParameters' in event_data and 'keyId' in event_data['requestParameters']:
                        used_key_id = event_data['requestParameters']['keyId']
                    elif 'requestParameters' in event_data and 'keyIdList' in event_data['requestParameters']:
                        # For operations like DisableKey, EnableKey, CancelKeyDeletion which take a list
                        for k_id in event_data['requestParameters']['keyIdList']:
                            if key_id_filter in k_id:
                                used_key_id = k_id
                                break
                    # Look for KeyId in responseElements (e.g. for CreateKey)
                    elif 'responseElements' in event_data and 'keyMetadata' in event_data['responseElements']:
                         if 'arn' in event_data['responseElements']['keyMetadata']:
                            used_key_id = event_data['responseElements']['keyMetadata']['arn']

                    # Check resources if keyId is not directly in params/elements
                    if not used_key_id and 'resources' in event_data:
                        for resource in event_data['resources']:
                            if resource.get('resourceType') == 'AWS::KMS::Key' and 'resourceName' in resource:
                                if key_id_filter in resource['resourceName']:
                                    used_key_id = resource['resourceName']
                                    break

                    if used_key_id and key_id_filter in used_key_id:
                        event_time = event.get('EventTime')
                        event_name = event.get('EventName')
                        user_identity = event_data.get('userIdentity', {})
                        username = user_identity.get('userName', user_identity.get('sessionContext', {}).get('sessionIssuer', {}).get('userName', 'N/A'))
                        source_ip = event_data.get('sourceIPAddress', 'N/A')

                        summaries.append(KeyUsageSummary(
                            key_id=used_key_id,
                            event_name=event_name,
                            event_time=event_time,
                            username=username,
                            source_ip=source_ip
                        ))
            
            next_token = response.get('NextToken')
            if not next_token:
                break
        except Exception as e:
            # Log errors appropriately in a real application
            print(f"Error looking up CloudTrail events: {e}")
            break

    return summaries