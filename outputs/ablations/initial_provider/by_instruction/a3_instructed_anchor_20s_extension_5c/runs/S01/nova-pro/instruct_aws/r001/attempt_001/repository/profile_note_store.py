import boto3

def store_profile_note(user_id, note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserProfileNotes')
    table.put_item(
        Item={
            'UserId': user_id,
            'Note': note
        }
    )