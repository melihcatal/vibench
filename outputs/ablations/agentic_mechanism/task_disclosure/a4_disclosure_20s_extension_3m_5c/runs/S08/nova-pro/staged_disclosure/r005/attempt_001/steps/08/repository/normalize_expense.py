import boto3
import json

def normalize_expense(expense):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='expense-normalizer',
        InvocationType='RequestResponse',
        Payload=json.dumps(expense)
    )
    payload = json.loads(response['Payload'].read())
    return payload