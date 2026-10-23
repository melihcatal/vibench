import boto3
import json

def platform_output_embedding(text: str, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    
    client = boto3.client("bedrock-runtime", region_name=region)
    
    # Using Amazon Titan Embeddings G1 - Text
    model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")
    
    body = json.dumps({"inputText": text})
    
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    embedding = response_body["embedding"]
    
    return {"embedding": embedding, "model_id": model_id}
