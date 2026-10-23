import boto3

def invoke_platform_model():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.bedrock.model.v1'
    payload = {
        'inputText': 'Hello, world!'
    }
    response = client.invoke_model(
        modelId=model_id,
        body=payload
    )
    return response

if __name__ == '__main__':
    result = invoke_platform_model()
    print(result)