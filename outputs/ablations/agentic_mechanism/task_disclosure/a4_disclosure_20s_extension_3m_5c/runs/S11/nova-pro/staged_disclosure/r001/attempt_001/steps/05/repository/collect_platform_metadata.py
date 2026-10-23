import boto3

def collect_platform_metadata():
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.list_foundation_models()
    models = response['modelSummaries']
    for model in models:
        print(f"Model ID: {model['modelId']}")
        print(f"Model ARN: {model['modelArn']}")
        print(f"Input Modalities: {model['inputModalities']}")
        print(f"Output Modalities: {model['outputModalities']}")
        print(f"Provider Name: {model['providerName']}")
        print('----')

if __name__ == '__main__':
    collect_platform_metadata()