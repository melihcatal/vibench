from __future__ import annotations

import json
from typing import Any, Dict

import cohere

from storage_client import get_cohere_api_key
from storage_models import EmbeddingResult


COHERE_EMBED_MODEL = "embed-english-v3.0"


def embed_asset_metadata(metadata: Dict[str, Any], extracted_text: str) -> EmbeddingResult:
    client = cohere.Client(get_cohere_api_key())
    payload = json.dumps(metadata, sort_keys=True, default=str)
    text = f"metadata: {payload}\ncontent: {extracted_text}"
    response = client.embed(texts=[text], model=COHERE_EMBED_MODEL, input_type="search_document")
    vector = list(response.embeddings[0])
    return EmbeddingResult(vector=vector, dimensions=len(vector), model=COHERE_EMBED_MODEL)
