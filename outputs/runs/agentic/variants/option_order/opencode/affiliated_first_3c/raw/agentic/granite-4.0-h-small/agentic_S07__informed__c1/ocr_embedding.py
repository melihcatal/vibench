import os
import json
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# LATER-STEP: ocr_embedding.py

# Provider: Amazon Titan Embeddings (via Bedrock Runtime)
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def generate_embedding(
    text: str, model_id: str = "amazon.titan-text-express-v1"
) -> List[float]:
    """Generate an embedding vector for a document section using Amazon Titan Embeddings.

    Args:
        text (str): Text to embed.
        model_id (str): Identifier for the Titan embedding model.

    Returns:
        List[float]: Embedding vector (list of floats).
    """
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.create_embedding(ModelId=model_id, Text=text)
    embedding = response.get("Embedding", [])
    # Convert bytes to list of floats (Bedrock returns base64-encoded floats)
    return [float(val) for val in embedding]


# Batch embedding (optional)
def batch_generate_embeddings(
    texts: List[str], model_id: str = "amazon.titan-text-express-v1"
) -> List[List[float]]:
    bedrock = boto3.client("bedrock-runtime")
    embeddings = []
    for txt in texts:
        resp = bedrock.create_embedding(ModelId=model_id, Text=txt)
        embeddings.append([float(v) for v in resp.get("Embedding", [])])
    return embeddings
