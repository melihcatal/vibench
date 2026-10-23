import boto3

bedrock = boto3.client('bedrock-runtime')

def collect_platform_metadata(model_id, payload):
    response = bedrock.invoke_model(
        modelId=model_id,
        body=payload
    )
    return {
        'output': response['body'].read(),
        'metadata': response['metadata']
    }