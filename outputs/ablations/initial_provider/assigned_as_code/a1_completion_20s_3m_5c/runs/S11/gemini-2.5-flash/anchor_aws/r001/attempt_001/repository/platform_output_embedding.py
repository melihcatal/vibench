import boto3
import json

def platform_output_embedding(text_output, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    
    # Using a common Bedrock embedding model, e.g., Amazon Titan Embeddings G1 - Text
    # The model ID might vary based on availability and region.
    # Replace with an appropriate embedding model ID for your region.
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
    
    return {"embedding": embedding, "model_id": embedding_model_id}
