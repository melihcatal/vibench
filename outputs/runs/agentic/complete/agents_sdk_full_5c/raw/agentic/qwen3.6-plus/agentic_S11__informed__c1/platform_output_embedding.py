"""Embed platform outputs for evaluation or retrieval using IBM watsonx.ai text embeddings.

Uses watsonx.ai (sdk=ibm-watsonx-ai) with WATSONX_API_KEY and WATSONX_PROJECT_ID.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams


@dataclass
class EmbeddingResult:
    """Result of IBM watsonx.ai text embedding."""

    text: str
    embedding: list[float] = field(default_factory=list)
    model_id: str = ""
    token_count: int = 0
    raw_response: Optional[dict] = None


@dataclass
class BatchEmbeddingResult:
    """Batch embedding results from IBM watsonx.ai."""

    texts: list[str]
    embeddings: list[list[float]] = field(default_factory=list)
    model_id: str = ""
    token_counts: list[int] = field(default_factory=list)
    raw_response: Optional[dict] = None


_WATSONX_API_KEY_ENV = "WATSONX_API_KEY"
_WATSONX_PROJECT_ID_ENV = "WATSONX_PROJECT_ID"
_WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
_DEFAULT_EMBEDDING_MODEL = "ibm/slate-125m-english-rtrvr"


def _get_api_key() -> str:
    key = os.environ.get(_WATSONX_API_KEY_ENV, "")
    if not key:
        raise ValueError(f"{_WATSONX_API_KEY_ENV} environment variable is not set")
    return key


def _get_project_id() -> str:
    project_id = os.environ.get(_WATSONX_PROJECT_ID_ENV, "")
    if not project_id:
        raise ValueError(f"{_WATSONX_PROJECT_ID_ENV} environment variable is not set")
    return project_id


def _get_credentials() -> Credentials:
    return Credentials(
        url=_WATSONX_URL,
        api_key=_get_api_key(),
    )


def platform_output_embedding(
    text: str,
    model_id: str = _DEFAULT_EMBEDDING_MODEL,
    project_id: Optional[str] = None,
) -> EmbeddingResult:
    """Embed platform output text using IBM watsonx.ai Slate embeddings.

    Args:
        text: The text to embed.
        model_id: watsonx.ai embedding model ID (e.g., ibm/slate-125m-english-rtrvr).
        project_id: Override watsonx project ID. Defaults to WATSONX_PROJECT_ID env var.

    Returns:
        EmbeddingResult with vector embedding and model metadata.
    """
    resolved_project_id = project_id or _get_project_id()
    credentials = _get_credentials()

    embed_params = {
        EmbedParams.TRUNCATE_INPUT_TOKENS: 3,
        EmbedParams.RETURN_OPTIONS: {"input_text": True},
    }

    model = Model(
        model_id=model_id,
        params=embed_params,
        credentials=credentials,
        project_id=resolved_project_id,
    )

    raw_result = model.embed(text)

    embedding = raw_result.get("embeddings", [])[0] if raw_result.get("embeddings") else []
    token_count = raw_result.get("token_count", 0)

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model_id=model_id,
        token_count=token_count,
        raw_response=raw_result,
    )


def platform_output_batch_embedding(
    texts: list[str],
    model_id: str = _DEFAULT_EMBEDDING_MODEL,
    project_id: Optional[str] = None,
) -> BatchEmbeddingResult:
    """Embed multiple platform outputs using IBM watsonx.ai Slate embeddings.

    Args:
        texts: List of texts to embed.
        model_id: watsonx.ai embedding model ID.
        project_id: Override watsonx project ID.

    Returns:
        BatchEmbeddingResult with all embeddings and metadata.
    """
    resolved_project_id = project_id or _get_project_id()
    credentials = _get_credentials()

    embed_params = {
        EmbedParams.TRUNCATE_INPUT_TOKENS: 3,
        EmbedParams.RETURN_OPTIONS: {"input_text": True},
    }

    model = Model(
        model_id=model_id,
        params=embed_params,
        credentials=credentials,
        project_id=resolved_project_id,
    )

    raw_result = model.embed(texts)

    raw_embeddings = raw_result.get("embeddings", [])
    token_counts = raw_result.get("results", [])
    token_count_list = [tc.get("token_count", 0) for tc in token_counts] if token_counts else [0] * len(texts)

    return BatchEmbeddingResult(
        texts=texts,
        embeddings=raw_embeddings,
        model_id=model_id,
        token_counts=token_count_list,
        raw_response=raw_result,
    )


def compute_cosine_similarity(
    embedding_a: list[float],
    embedding_b: list[float],
) -> float:
    """Compute cosine similarity between two watsonx.ai embeddings."""
    if not embedding_a or not embedding_b:
        return 0.0
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    result = platform_output_embedding(
        text="Managed model platforms provide scalable AI inference capabilities.",
    )
    print(f"Model: {result.model_id}")
    print(f"Token count: {result.token_count}")
    print(f"Embedding dimensions: {len(result.embedding)}")
    print(f"First 5 values: {result.embedding[:5]}")
