import boto3

def stream_platform_generation():
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': 'Hello, world!',
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    response_body = response['body'].read()
    response_text = response_body.decode('utf-8')
    print(response_text)
    
    return response