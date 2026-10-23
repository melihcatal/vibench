import boto3
from botocore.exceptions import ClientError

def store_audit_record(table_name, event):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=event)
        return True
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False