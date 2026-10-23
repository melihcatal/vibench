import boto3
import json

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using AWS Bedrock.
    """
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1' # Example region, can be configured
    )
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = json.dumps({
        "inputText": text
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding
