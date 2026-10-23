import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def embed_caption_chunk(caption_chunk):
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': caption_chunk
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    result = json.loads(response.get('body').read())
    embedding = result['embedding']

    return embedding