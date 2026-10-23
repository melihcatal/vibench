import boto3

def invoke_platform_model():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.titan-text-express-v1'
    input_text = 'Translate the following English text to French: Hello, how are you?'
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': input_text
        }
    )
    response_body = response['body'].read()
    return response_body