import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_rationale(rationale: str) -> dict:
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': rationale
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    result = json.loads(response.get('body').read())
    return result