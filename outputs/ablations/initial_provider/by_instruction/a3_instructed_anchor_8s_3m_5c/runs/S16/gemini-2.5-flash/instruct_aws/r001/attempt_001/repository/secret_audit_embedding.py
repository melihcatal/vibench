import json
from typing import List
from security_client import get_bedrock_runtime_client
from security_models import EmbeddingResult
import os

def embed_audit_notes(text: str, model_id: str = "amazon.titan-embed-text-v1") -> EmbeddingResult:
    """Embeds secret audit notes for semantic search using AWS Bedrock.

    Args:
        text: The audit note text to embed.
        model_id: The ID of the embedding model to use (e.g., "amazon.titan-embed-text-v1").

    Returns:
        An EmbeddingResult object containing the original text and its embedding.
    """
    client = get_bedrock_runtime_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    body = json.dumps({"inputText": text})
    accept = "application/json"
    content_type = "application/json"

    try:
        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept=accept,
            contentType=content_type
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get("embedding")
        if not embedding:
            raise ValueError("Embedding not found in the model response.")

        return EmbeddingResult(text=text, embedding=embedding)
    except Exception as e:
        raise RuntimeError(f"Error generating embedding with AWS Bedrock model {model_id}: {e}")
