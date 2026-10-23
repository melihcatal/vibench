from security_client import SecurityClient

class KeyUsageSummaryRequest:
    def __init__(self, key_id: str = None):
        self.key_id = key_id

class KeyUsageSummaryResponse:
    def __init__(self, key_summaries: list, key_details: dict = None):
        self.key_summaries = key_summaries
        self.key_details = key_details

def get_key_usage_summary(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    key_summaries = []
    paginator = kms_client.get_paginator('list_keys')
    for page in paginator.paginate():
        for key in page['Keys']:
            key_summaries.append({
                'KeyId': key['KeyId'],
                'KeyArn': key['KeyArn']
            })

    key_details = None
    if request.key_id:
        try:
            describe_key_response = kms_client.describe_key(KeyId=request.key_id)
            key_details = describe_key_response['KeyMetadata']
        except Exception as e:
            key_details = {'error': str(e)}

    return KeyUsageSummaryResponse(
        key_summaries=key_summaries,
        key_details=key_details
    )