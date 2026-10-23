import boto3

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

bedrock = boto3.client('bedrock-runtime', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def moderation_reason_embedding(text):
    response = bedrock.invoke_model(model_id='amazon.titan-embed-text-v1', body=text)
    return response['embedding']