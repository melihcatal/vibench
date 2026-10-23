import boto3

def profile_note_store(user_id, note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    table.put_item(Item={'user_id': user_id, 'note': note})