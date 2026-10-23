import boto3

def invoke_bedrock_model():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.titan-text-express-v1'
    payload = {
        'inputText': 'Hello, world!',
        'textGenerationConfig': {
            'maxTokenCount': 50,
            'stopSequences': [],
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload)
    )
    response_body = json.loads(response['body'].read())
    return response_body

if __name__ == '__main__':
    result = invoke_bedrock_model()
    print(result)