import boto3

def store_onboarding_notes(user_id, notes):
    client = boto3.client('dynamodb', region_name='us-west-2')
    client.put_item(
        TableName='OnboardingNotes',
        Item={'UserId': {'S': user_id}, 'Notes': {'S': notes}}
    )