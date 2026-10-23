import os
import json
import uuid
from typing import Optional, List, Dict
from datetime import datetime

import openai

from security_models import AuditEmbedding

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_HOST = "api.openai.com"


def embed_audit_note(
    audit_text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> AuditEmbedding:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    response = client.embeddings.create(
        model=model,
        input=audit_text,
    )

    embedding_data = response.data[0]
    embedding_id = str(uuid.uuid4())

    return AuditEmbedding(
        text=audit_text,
        embedding=embedding_data.embedding,
        model=model,
        metadata=metadata,
        embedding_id=embedding_id,
    )


def embed_audit_notes_batch(
    audit_texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    metadatas: Optional[List[Dict]] = None,
) -> List[AuditEmbedding]:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    response = client.embeddings.create(
        model=model,
        input=audit_texts,
    )

    embeddings = []
    for i, embedding_data in enumerate(response.data):
        metadata = metadatas[i] if metadatas and i < len(metadatas) else None
        embedding_id = str(uuid.uuid4())
        embeddings.append(
            AuditEmbedding(
                text=audit_texts[i],
                embedding=embedding_data.embedding,
                model=model,
                metadata=metadata,
                embedding_id=embedding_id,
            )
        )

    return embeddings


def embed_crypto_audit_log(
    audit_entries: List[Dict],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[AuditEmbedding]:
    texts = []
    metadatas = []

    for entry in audit_entries:
        text_parts = []
        if "action" in entry:
            text_parts.append(f"Action: {entry['action']}")
        if "key_id" in entry:
            text_parts.append(f"Key ID: {entry['key_id']}")
        if "timestamp" in entry:
            text_parts.append(f"Timestamp: {entry['timestamp']}")
        if "principal" in entry:
            text_parts.append(f"Principal: {entry['principal']}")
        if "source_ip" in entry:
            text_parts.append(f"Source IP: {entry['source_ip']}")
        if "details" in entry:
            text_parts.append(f"Details: {entry['details']}")
        if "result" in entry:
            text_parts.append(f"Result: {entry['result']}")

        combined_text = " | ".join(text_parts) if text_parts else json.dumps(entry)
        texts.append(combined_text)
        metadatas.append(entry)

    return embed_audit_notes_batch(
        texts, model=model, api_key=api_key, metadatas=metadatas
    )


def search_similar_audit_notes(
    query_text: str,
    stored_embeddings: List[AuditEmbedding],
    model: str = OPENAI_EMBEDDING_MODEL,
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Dict]:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    query_response = client.embeddings.create(
        model=model,
        input=query_text,
    )
    query_embedding = query_response.data[0].embedding

    scored_results = []
    for stored in stored_embeddings:
        similarity = cosine_similarity(query_embedding, stored.embedding)
        scored_results.append(
            {
                "embedding_id": stored.embedding_id,
                "text": stored.text,
                "similarity": similarity,
                "metadata": stored.metadata,
            }
        )

    scored_results.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_results[:top_k]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def serialize_embedding(embedding: AuditEmbedding) -> Dict:
    return embedding.to_dict()


def deserialize_embedding(data: Dict) -> AuditEmbedding:
    return AuditEmbedding(
        text=data["text"],
        embedding=data["embedding"],
        model=data["model"],
        metadata=data.get("metadata"),
        embedding_id=data.get("embedding_id"),
    )
