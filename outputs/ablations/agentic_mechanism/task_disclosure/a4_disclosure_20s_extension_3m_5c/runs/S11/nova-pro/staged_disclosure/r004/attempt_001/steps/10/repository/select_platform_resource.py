import boto3

def select_platform_resource():
    bedrock_client = boto3.client('bedrock')
    # Example: Retrieve a list of available models
    response = bedrock_client.list_models()
    return response

if __name__ == '__main__':\n    print(select_platform_resource())