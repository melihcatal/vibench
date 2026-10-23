import boto3

client = boto3.client('bedrock-runtime', region_name='us-west-2')

def summarize_incident(logs):
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': '\n'.join(logs),
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response['body'].read().decode()