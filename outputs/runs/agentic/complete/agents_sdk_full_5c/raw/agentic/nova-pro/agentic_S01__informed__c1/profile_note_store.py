import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def store_note(user_id, note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ProfileNotes')
    table.put_item(Item={'UserID': user_id, 'Note': note})
    return 'Note stored successfully'