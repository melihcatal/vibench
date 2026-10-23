import boto3

def collect_platform_metadata():
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
    metadata = {
        'model_id': model_id,
        'response': response_body
    }
    return metadata