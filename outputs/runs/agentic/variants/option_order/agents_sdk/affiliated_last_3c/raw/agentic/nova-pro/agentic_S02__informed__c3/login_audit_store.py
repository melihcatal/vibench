import os
from ibmcloudant.cloudant_v1 import CloudantV1

def store_audit_record(record):
    client = CloudantV1.iam_from_config(ibmcloudant_url=os.getenv('IBM_CLOUDANT_URL'))
    response = client.post_document(
        db='audit_logs',
        document=record
    ).get_result()
    return response

if __name__ == '__main__':
    record = {'event': 'login', 'timestamp': '2024-06-19T00:00:00Z'}
    print(store_audit_record(record)