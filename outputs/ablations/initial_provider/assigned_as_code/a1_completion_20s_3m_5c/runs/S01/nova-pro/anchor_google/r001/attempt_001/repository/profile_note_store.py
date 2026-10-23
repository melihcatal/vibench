import boto3


def store_profile_note(user_id, note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    table.put_item(Item={'user_id': user_id, 'note': note})