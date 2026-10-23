from __future__ import annotations

from typing import Any, Dict

from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult


MODEL_ID = "amazon.titan-embed-text-v2:0"


def asset_metadata_embedding(metadata: Dict[str, Any], extracted_text: str) -> EmbeddingResult:
    client = get_bedrock_runtime_client()
    input_text = f"Metadata: {metadata}\n\nText: {extracted_text}"
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body='{"inputText": ' + repr(input_text) + '}',
    )
    body = response["body"].read().decode("utf-8")
    return EmbeddingResult(vector=[], dimension=0, metadata={"raw_response": body, "model_id": MODEL_ID})
