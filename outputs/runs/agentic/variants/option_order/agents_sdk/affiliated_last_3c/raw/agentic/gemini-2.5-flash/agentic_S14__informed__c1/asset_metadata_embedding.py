import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingsRequest, EmbeddingsResponse
from typing import List

def embed_asset_metadata_and_text(request: EmbeddingsRequest) -> EmbeddingsResponse:
    """Embeds object metadata and extracted text for search using Amazon Bedrock with the Titan Embeddings model.

    Args:
        request: An EmbeddingsRequest containing a list of strings to embed.

    Returns:
        An EmbeddingsResponse with a list of generated embeddings.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    all_embeddings: List[List[float]] = []

    for text_to_embed in request.text_to_embed:
        body = json.dumps({
            "inputText": text_to_embed
        })

        model_id = "amazon.titan-embed-text-v1"
        accept = "application/json"
        content_type = "application/json"

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept=accept,
            contentType=content_type
        )

        response_body = json.loads(response.get('body').read())
        embedding = response_body['embedding']
        all_embeddings.append(embedding)

    return EmbeddingsResponse(embeddings=all_embeddings)
