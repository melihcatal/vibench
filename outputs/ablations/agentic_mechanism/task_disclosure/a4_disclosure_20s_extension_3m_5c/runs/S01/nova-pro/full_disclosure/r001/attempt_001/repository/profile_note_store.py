import boto3

def store_onboarding_notes(user_id, notes):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    table.put_item(
        Item={
            'user_id': user_id,
            'notes': notes
        }
    )

def get_onboarding_notes(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    response = table.get_item(
        Key={'user_id': user_id}
    )
    return response.get('Item', None)