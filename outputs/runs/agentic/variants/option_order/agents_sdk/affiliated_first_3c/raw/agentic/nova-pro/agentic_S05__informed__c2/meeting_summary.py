import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

def summarize_meeting(text):
    response = bedrock.invoke_model(modelId='amazon.titan-text-express-v1', body=text)
    return response
