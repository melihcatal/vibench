import boto3
import os
import json
from typing import List

def get_bedrock_embeddings(text: str, model_id: str = "amazon.titan-embed-text-v1") -> List[float]:
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    body = json.dumps({"inputText": text})
    
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    if not embedding:
        raise ValueError("Embedding not found in the response.")
        
    return embedding

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # export AWS_SECRET_ACCESS_KEY="your-secret-key"
    # export AWS_REGION="your-aws-region" (e.g., us-west-2, as titan-embed is not in all regions)

    text_to_embed = "This is a sample text for embedding."
    try:
        embeddings = get_bedrock_embeddings(text_to_embed)
        print(f"Embeddings for '{text_to_embed[:30]}...': {embeddings[:5]}...") # Print first 5 dimensions
        print(f"Length of embeddings: {len(embeddings)}")
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        print("Please ensure you have access to amazon.titan-embed-text-v1 in your AWS region.")
