import os
import json
from typing import List, Dict, Any

# Direct Embeddings example: Amazon Titan Embeddings via Bedrock Runtime
# Uses boto3 SDK for embedding generation


def embed_segments(segments: List[str]) -> List[Dict[str, Any]]:
    """Generate embeddings for a list of translated segments using Amazon Titan.

    Args:
        segments: List of text strings to embed.

    Returns:
        List of dicts, each containing an 'id' and 'embedding' vector (list of floats).
    """
    # Boto3 client for Bedrock
    import boto3

    # Ensure AWS credentials are available
    region_name = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise RuntimeError("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set")

    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    # Titan text embeddings model ID (example ID – replace with actual if needed)
    model_id = "amazon.titan-text-express-v1"

    embeddings = []
    for idx, segment in enumerate(segments):
        # Call the Bedrock endpoint for embeddings
        response = bedrock.invoke_endpoint(
            EndpointName=model_id,
            ContentType="application/json",
            Body=json.dumps({"inputs": [segment]}),
        )
        # Response Body is a JSON string per Bedrock docs
        payload = json.loads(response["Body"].read().decode())
        # Extract the embedding vector; structure may vary by model version
        vec = payload.get("results", [{}])[0].get("embeddings", [None])[0]
        embeddings.append({"id": idx, "embedding": vec})
    return embeddings


# Simple demonstration when executed directly (requires AWS credentials)
if __name__ == "__main__":
    texts = ["Hello, world!", "Python is great."]
    vecs = embed_segments(texts)
    for idx, vec in vecs:
        print(f"Segment {idx}: {vec[:5]}... (total {_len(vec)} dims)")
