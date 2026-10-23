# [LATER-STEP] secret_audit_embedding.py
# Embed secret audit notes for semantic search using Amazon Bedrock Titan embeddings

import os
import boto3
import json
from fetch_api_key import fetch_api_key
from fetch_db_secret import fetch_db_secret


def embed_audit_note(secret_name: str, note: str) -> str:
    """Create an embedding for an audit note and store it alongside the secret."""
    # Retrieve the model ID for Titan Text Embedding (v1)
    embed_model = "amazon.titan-text-embed-v1"
    # Initialise Bedrock runtime client
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url="https://bedrock.us-east-1.amazonaws.com",
    )
    # Call the embeddings API
    payload = {"inputs": [{"input": {"text": note}}], "modelId": embed_model}
    response = bedrock.post_model_input(modelId=embed_model, body=json.dumps(payload))
    # The response contains a base64 encoded embedding vector
    embedding_b64 = json.loads(response["body"].read().decode())["embeddings"][0][
        "embedding"
    ]
    embedding = base64.b64decode(embedding_b64).tolist()
    # Store the embedding back to a metadata store (placeholder implementation)
    metadata = {"secret_name": secret_name, "note": note, "embedding": embedding}
    # In a real system you would upsert this JSON to a vector DB (e.g., Amazon OpenSearch, Pinecone)
    return "embedding_stored"
