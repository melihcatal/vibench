import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"), base_url=base_url or os.getenv("OPENAI_BASE_URL"))


def get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_texts(texts: Sequence[str], model: Optional[str] = None, dimensions: Optional[int] = None, api_key: Optional[str] = None, base_url: Optional[str] = None) -> List[List[float]]:
    client = get_openai_client(api_key=api_key, base_url=base_url)
    params: Dict[str, Any] = {"model": model or get_embedding_model(), "input": list(texts)}
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    return [item.embedding for item in response.data]


def embed_text(text: str, model: Optional[str] = None, dimensions: Optional[int] = None, api_key: Optional[str] = None, base_url: Optional[str] = None) -> List[float]:
    return embed_texts([text], model=model, dimensions=dimensions, api_key=api_key, base_url=base_url)[0]


def build_embedding_request(texts: Sequence[str], model: Optional[str] = None, dimensions: Optional[int] = None) -> Dict[str, Any]:
    request: Dict[str, Any] = {"model": model or get_embedding_model(), "input": list(texts)}
    if dimensions is not None:
        request["dimensions"] = dimensions
    return request


def normalize_texts(texts: Union[str, Iterable[str]]) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    return [str(text) for text in texts]
