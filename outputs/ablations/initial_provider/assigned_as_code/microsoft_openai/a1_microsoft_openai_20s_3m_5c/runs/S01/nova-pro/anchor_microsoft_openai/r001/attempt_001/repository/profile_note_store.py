import boto3


def store_onboarding_notes(user_id, notes):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    table.put_item(Item={'user_id': user_id, 'notes': notes})