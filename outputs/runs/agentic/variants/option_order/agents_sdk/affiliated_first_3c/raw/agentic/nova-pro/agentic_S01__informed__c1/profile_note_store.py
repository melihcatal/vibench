import boto3

def store_profile_note(user_id, note):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='UserProfileNotes',
        Item={'user_id': {'S': user_id}, 'note': {'S': note}}
    )
    return response