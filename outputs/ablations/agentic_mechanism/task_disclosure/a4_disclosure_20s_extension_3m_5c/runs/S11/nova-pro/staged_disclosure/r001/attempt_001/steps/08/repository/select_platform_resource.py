import boto3

bedrock = boto3.client('bedrock-runtime')

def select_platform_resource():
    model_id = 'amazon.titan-text-express-v1'
    response = bedrock.invoke_model(
        modelId=model_id,
        body={
            'inputText': 'Hello, world!'
        }
    )
    result = json.loads(response['body'].read())
    return result

if __name__ == '__main__':
    print(select_platform_resource())