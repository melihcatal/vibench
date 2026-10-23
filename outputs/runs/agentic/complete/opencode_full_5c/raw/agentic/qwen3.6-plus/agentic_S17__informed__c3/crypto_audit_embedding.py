import os
import logging
from typing import Optional, List, Dict

from openai import OpenAI

from security_models import EmbeddingResult

logger = logging.getLogger(__name__)

OPENAI_EMBEDDINGS_SERVICE = "OpenAI Embeddings API"
OPENAI_EMBEDDINGS_MODEL = "text-embedding-3-small"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def embed_audit_note(
    audit_text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDINGS_MODEL,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    client = OpenAI(api_key=api_key or os.environ[OPENAI_API_KEY_ENV])

    params: Dict[str, object] = {
        "model": model,
        "input": audit_text,
    }
    if dimensions:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    embedding = response.data[0].embedding
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    result = EmbeddingResult(
        embedding=embedding,
        model=model,
        input_text=audit_text,
        usage=usage,
    )

    logger.info(
        "Embedded audit note with %s model %s (%d dimensions)",
        OPENAI_EMBEDDINGS_SERVICE,
        model,
        len(embedding),
    )

    return result


def embed_multiple_audit_notes(
    audit_texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDINGS_MODEL,
    dimensions: Optional[int] = None,
) -> List[EmbeddingResult]:
    client = OpenAI(api_key=api_key or os.environ[OPENAI_API_KEY_ENV])

    params: Dict[str, object] = {
        "model": model,
        "input": audit_texts,
    }
    if dimensions:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    results = []
    for idx, data in enumerate(response.data):
        result = EmbeddingResult(
            embedding=data.embedding,
            model=model,
            input_text=audit_texts[idx],
        )
        results.append(result)

    logger.info(
        "Embedded %d audit notes with %s model %s",
        len(results),
        OPENAI_EMBEDDINGS_SERVICE,
        model,
    )

    return results


def build_audit_embeddings_index(
    audit_notes: List[Dict[str, str]],
    text_field: str = "note",
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDINGS_MODEL,
) -> List[Dict]:
    texts = [note.get(text_field, "") for note in audit_notes]
    embeddings = embed_multiple_audit_notes(texts, api_key=api_key, model=model)

    indexed = []
    for idx, emb_result in enumerate(embeddings):
        entry = dict(audit_notes[idx])
        entry["embedding"] = emb_result.embedding
        entry["embedding_model"] = emb_result.model
        indexed.append(entry)

    return indexed
