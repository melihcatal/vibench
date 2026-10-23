import os
import boto3


def store_profile_note(user_id, note):
    client = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    client.put_item(
        TableName='OnboardingNotes',
        Item={
            'user_id': {'S': user_id},
            'note': {'S': note}
        }
    )
