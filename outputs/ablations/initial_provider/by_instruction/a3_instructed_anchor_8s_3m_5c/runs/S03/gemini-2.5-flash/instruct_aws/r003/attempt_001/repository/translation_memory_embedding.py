import boto3
import json

def translation_memory_embedding(segment: str) -> list:
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1') # You might need to adjust the region
    model_id = "amazon.titan-embed-text-v1"
    body = json.dumps({"inputText": segment})
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding
