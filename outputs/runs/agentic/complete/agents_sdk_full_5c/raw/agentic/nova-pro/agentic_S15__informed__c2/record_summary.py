import boto3

anthropic = boto3.client('bedrock-runtime')

def summarize_record(text):
    response = anthropic.invoke_model(
        modelId='anthropic.claude-v2',
        body={
            'prompt': f'Summarize the following text: {text}',
            'max_tokens_to_sample': 300
        }
    )
    return response['body'].read().decode('utf-8')