import os
import json
from typing import List
from security_client import get_bedrock_runtime_client


def embed_audit_notes(notes: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search using Amazon Titan Embeddings via Bedrock Runtime.
    """
    client = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": notes})

    try:
        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")
        if not embedding:
            raise ValueError("Embedding not found in the response.")
        return embedding
    except Exception as e:
        raise RuntimeError(f"Error embedding audit notes with Bedrock: {e}")
