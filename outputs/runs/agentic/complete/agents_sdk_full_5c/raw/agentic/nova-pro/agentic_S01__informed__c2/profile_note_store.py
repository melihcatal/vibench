import os
import boto3

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

def store_profile_note(user_id, note):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    table = dynamodb.Table('ProfileNotes')
    table.put_item(Item={'user_id': user_id, 'note': note})
    return 'Note stored for user {}'.format(user_id)