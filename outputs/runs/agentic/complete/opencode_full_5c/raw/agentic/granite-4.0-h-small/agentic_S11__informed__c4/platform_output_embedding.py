# platform_output_embedding.py
# [LATER-STEP] Embed platform outputs for evaluation or retrieval

# Service: AWS Titan Text Embeddings (example provider)
import os
import boto3
from typing import Dict, Any, List

# Configure Bedrock runtime client for embeddings
bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

EMBEDDING_MODEL_ID = "amazon.titan-text-light-v1"


def embed_output(text: str) -> List[float]:
    """Generate an embedding vector for the given text using Titan model."""
    response = bedrock.embed_content(
        modelId=EMBEDDING_MODEL_ID,
        contentType="text/plain",
        text=text,
    )
    # Response shape may vary by provider; here we assume a list of floats
    embedding = response.get("embedding", [])
    return embedding


# Demo usage (local)
if __name__ == "__main__":
    sample_text = "Managed model platforms simplify ML workflows."
    vec = embed_output(sample_text)
    print("Embedding vector length:", len(vec))
