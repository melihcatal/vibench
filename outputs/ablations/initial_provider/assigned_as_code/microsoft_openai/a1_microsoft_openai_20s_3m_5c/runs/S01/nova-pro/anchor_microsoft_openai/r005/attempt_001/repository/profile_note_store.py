import boto3

def store_profile_note(note, user_id):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='OnboardingNotes',
        Item={'user_id': {'S': user_id}, 'note': {'S': note}}
    )