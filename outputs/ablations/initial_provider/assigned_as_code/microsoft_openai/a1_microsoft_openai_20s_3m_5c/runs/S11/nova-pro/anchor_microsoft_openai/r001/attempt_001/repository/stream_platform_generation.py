import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_platform_generation(model_id, payload):
    response = bedrock.invoke_model(
        modelId=model_id,
        body=payload
    )
    for event in response['body']:
        yield event