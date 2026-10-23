import boto3

def collect_platform_metadata(model_id, input_text):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(
        model_id=model_id,
        body={
            'inputText': input_text
        }
    )
    model_output = response['outputText']
    usage = response['usage']
    resource_id = response['responseMetadata']['RequestId']
    return {
        'model_output': model_output,
        'usage': usage,
        'resource_id': resource_id
    }

if __name__ == '__main__':
    model_id = 'amazon.titan-text-express-v1'
    input_text = 'Translate this text to French.'
    metadata = collect_platform_metadata(model_id, input_text)
    print(metadata)