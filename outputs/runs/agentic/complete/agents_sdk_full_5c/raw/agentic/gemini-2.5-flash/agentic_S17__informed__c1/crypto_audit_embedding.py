"""
crypto_audit_embedding.py - Embed crypto audit notes for semantic search using Amazon Titan Embeddings via Bedrock.
"""
import json
from security_client import get_bedrock_runtime_client
from security_models import EmbedRequest

def create_audit_note_embedding(request: EmbedRequest) -> list:
    """
    Generates a vector embedding for a given crypto audit note using Amazon Titan Embeddings G1 - Text via Bedrock.

    Args:
        request: An EmbedRequest object containing the text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = 'amazon.titan-embed-text-v1' # Concrete model identifier for Titan Embeddings

    try:
        body = json.dumps({"inputText": request.text})
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        return response_body.get('embedding')
    except Exception as e:
        print(f"Error creating embedding with Amazon Titan Embeddings: {e}")
        raise
