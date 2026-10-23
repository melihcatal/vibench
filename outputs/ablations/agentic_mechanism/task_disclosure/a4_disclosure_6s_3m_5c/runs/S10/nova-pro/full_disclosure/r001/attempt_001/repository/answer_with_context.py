import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

bedrock_client = boto3.client('bedrock-runtime')

def answer_with_context(question, context):
    try:
        response = bedrock_client.invoke_model(
            model_id='amazon.bedrock.<model_id>',
            body={
                'prompt': f'Answer the following question using the provided context: {question}\n\nContext: {context}',
                'max_tokens': 150
            }
        )
        result = response['body'].read()
        return result.decode('utf-8')
    except (NoCredentialsError, PartialCredentialsError) as e:
        return f'Error: {e}'