import boto3

def summarize_onboarding_state(user_id):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body={
            'inputText': f'Summarize onboarding state for user {user_id}'
        }
    )
    return response['Body'].read().decode('utf-8')