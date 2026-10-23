import boto3

def embed_platform_output(output):
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.titan-embed-text-v1'
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': output
        }
    )
    response_body = response['body'].read()
    return response_body