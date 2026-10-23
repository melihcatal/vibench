from __future__ import annotations

from typing import Dict, List

from model_client import create_embedding
from model_models import coerce_text


def output_embedding(text: str, model: str = "text-embedding-3-small") -> Dict[str, List[float]]:
    result = create_embedding(coerce_text(text), model=model)
    return {"model": result.model, "embedding": result.vector}
