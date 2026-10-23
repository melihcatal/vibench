import boto3

def summarize_onboarding_state(user_id):
    client = boto3.client('dynamodb', region_name='us-west-2')
    response = client.get_item(
        TableName='OnboardingStates',
        Key={'UserId': {'S': user_id}}
    )
    return response.get('Item', {})