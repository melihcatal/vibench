import boto3

AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'

def moderation_summary(text):
    bedrock = boto3.client('bedrock-runtime', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = bedrock.invoke_model(model_id='amazon.titan-text-express-v1', body={
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 200,
            'temperature': 0.5,
            'topP': 0.9
        }
    })
    return response['body'].read().decode('utf-8')