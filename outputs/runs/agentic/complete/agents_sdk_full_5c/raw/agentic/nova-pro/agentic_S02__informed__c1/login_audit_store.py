import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def store_login_audit(event):
    client = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = client.put_item(
        TableName='LoginAudit',
        Item={
            'EventId': {'S': event['id']},
            'Timestamp': {'S': event['timestamp']},
            'UserId': {'S': event['user_id']},
            'EventType': {'S': event['event_type']}
        }
    )
    print(response)