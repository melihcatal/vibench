import os
from typing import List, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_script(script: str, model: str = "text-embedding-3-small") -> List[float]:
    response = _client().embeddings.create(model=model, input=script)
    return list(response.data[0].embedding)


def embed_scripts(scripts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    response = _client().embeddings.create(model=model, input=scripts)
    return [list(item.embedding) for item in response.data]


def script_embedding_for_search(script: str, voice_asset_id: Optional[str] = None) -> dict:
    payload = {"embedding": embed_script(script), "provider": "openai", "model": "text-embedding-3-small"}
    if voice_asset_id is not None:
        payload["voice_asset_id"] = voice_asset_id
    return payload
