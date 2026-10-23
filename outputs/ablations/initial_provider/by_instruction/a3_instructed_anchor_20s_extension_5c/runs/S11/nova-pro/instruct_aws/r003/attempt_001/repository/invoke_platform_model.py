import boto3

def invoke_model():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': 'Hello, world!',
            'textGenerationConfig': {
                'maxTokenCount': 500,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response