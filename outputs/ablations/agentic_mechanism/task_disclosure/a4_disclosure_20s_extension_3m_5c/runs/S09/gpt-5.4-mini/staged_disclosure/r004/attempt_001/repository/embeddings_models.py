import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

import requests


OPENAI_DIRECT_EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


EmbeddingInput = Union[str, Sequence[str]]


@dataclass
class EmbeddingsRequest:
    input: EmbeddingInput
    model: str = OPENAI_DEFAULT_EMBEDDING_MODEL
    user: Optional[str] = None
    dimensions: Optional[int] = None
    encoding_format: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": self.input, "model": self.model}
        if self.user is not None:
            payload["user"] = self.user
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        return payload


@dataclass
class EmbeddingsResponseData:
    index: int
    embedding: List[float]
    object: Optional[str] = None


@dataclass
class EmbeddingsResponse:
    data: List[EmbeddingsResponseData]
    model: Optional[str] = None
    object: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "EmbeddingsResponse":
        data = [
            EmbeddingsResponseData(
                index=item["index"],
                embedding=item["embedding"],
                object=item.get("object"),
            )
            for item in payload.get("data", [])
        ]
        return cls(
            data=data,
            model=payload.get("model"),
            object=payload.get("object"),
            usage=payload.get("usage"),
        )


def normalize_embedding(embedding: Sequence[float]) -> List[float]:
    return [float(value) for value in embedding]


def normalize_embeddings_response(payload: Dict[str, Any]) -> EmbeddingsResponse:
    response = EmbeddingsResponse.from_json(payload)
    response.data = [
        EmbeddingsResponseData(
            index=item.index,
            embedding=normalize_embedding(item.embedding),
            object=item.object,
        )
        for item in sorted(response.data, key=lambda item: item.index)
    ]
    return response


def load_embeddings_config() -> Dict[str, Any]:
    return {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": os.getenv("OPENAI_BASE_URL", OPENAI_DIRECT_EMBEDDINGS_API_URL),
        "model": os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_DEFAULT_EMBEDDING_MODEL),
        "timeout": float(os.getenv("OPENAI_EMBEDDINGS_TIMEOUT", "30")),
    }


def create_embeddings_request(
    input_texts: EmbeddingInput,
    model: Optional[str] = None,
    user: Optional[str] = None,
    dimensions: Optional[int] = None,
    encoding_format: Optional[str] = None,
) -> EmbeddingsRequest:
    config = load_embeddings_config()
    return EmbeddingsRequest(
        input=input_texts,
        model=model or config["model"],
        user=user,
        dimensions=dimensions,
        encoding_format=encoding_format,
    )


def post_embeddings_request(request_model: EmbeddingsRequest, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> EmbeddingsResponse:
    config = load_embeddings_config()
    response = requests.post(
        (base_url or config["base_url"]).rstrip("/"),
        headers={
            "Authorization": f"Bearer {api_key or config['api_key']}",
            "Content-Type": "application/json",
        },
        json=request_model.to_payload(),
        timeout=timeout if timeout is not None else config["timeout"],
    )
    response.raise_for_status()
    return normalize_embeddings_response(response.json())
