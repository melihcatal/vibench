import boto3

def collect_platform_metadata():
    bedrock_client = boto3.client('bedrock', region_name='us-west-2')
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': 'Hello, world!'
        }
    )
    model_output = response['body'].read()
    usage = response['usage']
    resource_id = response['responseMetadata']['RequestId']
    return {
        'model_output': model_output,
        'usage': usage,
        'resource_id': resource_id
    }

if __name__ == '__main__':
    metadata = collect_platform_metadata()
    print(metadata)