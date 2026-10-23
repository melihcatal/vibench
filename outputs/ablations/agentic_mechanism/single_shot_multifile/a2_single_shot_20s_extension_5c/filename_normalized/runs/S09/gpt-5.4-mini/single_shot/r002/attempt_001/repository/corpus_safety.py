import os
from typing import Dict, List

from openai import OpenAI

from embeddings_models import normalize_texts


_SAFE_DEFAULT_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_corpus_text(texts: List[str], api_key: str | None = None) -> Dict[str, object]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    normalized = normalize_texts(texts)
    response = client.moderations.create(input=normalized, model=_SAFE_DEFAULT_MODEL)
    data = response.model_dump()
    results = data.get("results", [])
    flagged = any(item.get("flagged", False) for item in results)
    return {"flagged": flagged, "results": results}
