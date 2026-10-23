from typing import List, Optional

from openai import OpenAI

from model_client import get_client, resolve_model_name
from model_models import normalize_text


def platform_output_embedding(text: str, model: Optional[str] = None) -> List[float]:
    client = get_client()
    embedding_model = model or "text-embedding-3-large"
    result = client.embeddings.create(model=embedding_model, input=normalize_text(text))
    return list(result.data[0].embedding)
