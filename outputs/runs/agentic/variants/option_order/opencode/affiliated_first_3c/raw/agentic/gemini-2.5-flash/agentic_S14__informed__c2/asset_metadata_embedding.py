import json
from typing import Dict, Any, List
from storage_client import get_bedrock_runtime_client


def embed_asset_metadata_and_text(text_to_embed: str) -> List[float]:
    """
    Embeds object metadata and extracted text for search using Amazon Titan Embeddings via Bedrock Runtime.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()

    body = json.dumps({"inputText": text_to_embed})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-text-v1",
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return embedding
