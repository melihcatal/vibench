import boto3

def stream_model_output(model_id):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body={
            'prompt': 'Generate a story about a magical forest.',
            'max_tokens': 500
        }
    )
    for event in response['body']:
        yield event

# Example usage:
# for event in stream_model_output('amazon.titan-text-express-v1'):
#     print(event)