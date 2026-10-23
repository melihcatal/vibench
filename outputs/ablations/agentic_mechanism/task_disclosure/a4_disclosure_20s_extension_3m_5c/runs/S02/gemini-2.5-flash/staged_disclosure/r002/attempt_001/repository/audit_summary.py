import boto3
import json

def summarize_federated_login_events():
    client = boto3.client('cloudtrail')

    try:
        response = client.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventSource',
                    'AttributeValue': 'signin.amazonaws.com'
                },
            ],
            MaxResults=50 # Adjust as needed
        )

        federated_login_events = []
        for event in response.get('Events', []):
            cloudtrail_event = json.loads(event['CloudTrailEvent'])
            # Look for events related to federated logins. This is a basic check.
            # Real-world scenarios might require more sophisticated parsing of eventData.
            if 'federated' in json.dumps(cloudtrail_event).lower() or \
               'federation' in json.dumps(cloudtrail_event).lower() or \
               cloudtrail_event.get('eventName') in ['ConsoleLogin', 'AssumeRoleWithWebIdentity', 'AssumeRoleWithSaml']:
                federated_login_events.append(cloudtrail_event)

        if federated_login_events:
            print("Summary of Federated Login Events:")
            for event in federated_login_events:
                print(f"  Event Name: {event.get('eventName')}")
                print(f"  Event Time: {event.get('eventTime')}")
                print(f"  User Identity: {event.get('userIdentity', {}).get('type')}, {event.get('userIdentity', {}).get('principalId')}")
                print(f"  Source IP Address: {event.get('sourceIPAddress')}")
                print("-" * 30)
        else:
            print("No federated login events found in the latest 50 CloudTrail events.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    summarize_federated_login_events()
