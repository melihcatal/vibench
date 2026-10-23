import boto3

def store_profile_note(user_id, note):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='OnboardingNotes',
        Item={
            'UserId': {'S': user_id},
            'Note': {'S': note}
        }
    )
    return response