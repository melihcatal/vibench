import boto3

def collect_platform_metadata():
    bedrock_client = boto3.client('bedrock', region_name='us-west-2')
    model_id = 'amazon.titan-text-express-v1'
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body={
            'inputText': 'Hello, world!'
        }
    )
    model_output = response['body'].read().decode('utf-8')
    usage = response['usage']
    resource_id = response['responseMetadata']['RequestId']
    model_handle = response['modelId']
    return {
        'model_output': model_output,
        'usage': usage,
        'resource_id': resource_id,
        'model_handle': model_handle
    }

if __name__ == '__main__':
    metadata = collect_platform_metadata()
    print(metadata)