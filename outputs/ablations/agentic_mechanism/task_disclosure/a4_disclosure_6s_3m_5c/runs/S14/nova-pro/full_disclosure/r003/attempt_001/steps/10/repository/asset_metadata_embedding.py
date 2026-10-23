import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def embed_metadata_and_text(metadata, extracted_text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': extracted_text,
        'textGranularity': 'LINE'
    }
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding