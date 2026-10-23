import boto3

def rotation_summary(secret_name):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': f'Summarize the rotation status of secret {secret_name}'
        }
    )
    return response['body']['summary']