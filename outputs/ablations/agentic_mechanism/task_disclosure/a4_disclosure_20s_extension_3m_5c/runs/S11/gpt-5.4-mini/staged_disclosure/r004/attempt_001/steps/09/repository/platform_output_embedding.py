import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def _normalize_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _chunk_text(text: str, max_chars: int = 12000) -> List[str]:
    text = text.strip()
    if not text:
        return [""]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


class PlatformOutputEmbedder:
    def __init__(self, model: str = "text-embedding-3-large") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_texts(self, texts: Sequence[str]) -> List[List[float]]:
        cleaned = [_normalize_text(text) for text in texts]
        response = self.client.embeddings.create(model=self.model, input=cleaned)
        return [item.embedding for item in response.data]

    def embed_platform_output(self, platform_output: object) -> List[List[float]]:
        text = _normalize_text(platform_output)
        chunks = _chunk_text(text)
        return self.embed_texts(chunks)

    def embed_for_retrieval(self, platform_outputs: Iterable[object]) -> List[List[float]]:
        flattened: List[str] = []
        for output in platform_outputs:
            flattened.extend(_chunk_text(_normalize_text(output)))
        return self.embed_texts(flattened)


def embed_platform_output(platform_output: object, model: str = "text-embedding-3-large") -> List[List[float]]:
    return PlatformOutputEmbedder(model=model).embed_platform_output(platform_output)


def embed_platform_outputs(platform_outputs: Iterable[object], model: str = "text-embedding-3-large") -> List[List[float]]:
    return PlatformOutputEmbedder(model=model).embed_for_retrieval(platform_outputs)
