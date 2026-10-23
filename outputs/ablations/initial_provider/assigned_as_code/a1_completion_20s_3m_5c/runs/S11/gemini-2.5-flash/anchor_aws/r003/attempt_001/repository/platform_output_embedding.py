import boto3
import json

def platform_output_embedding(text_output, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    
    # Using a common Amazon embedding model. Adjust modelId as needed.
    embedding_model_id = "amazon.titan-embed-text-v1"
    
    body = json.dumps({"inputText": text_output})
    
    response = client.invoke_model(
        body=body,
        modelId=embedding_model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response["body"].read())
    embedding = response_body["embedding"]
    
    return {"embedding": embedding, "model_id": embedding_model_id, "_original_response_body": response_body}
