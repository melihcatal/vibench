from __future__ import annotations

from dataclasses import dataclass
from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingModel


@dataclass
class AuditEmbedding:
    vector: List[float]
    model_name: str


def crypto_audit_embedding(notes: str) -> AuditEmbedding:
    vertexai.init(project="demo-project", location="us-central1")
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embedding = model.get_embeddings([notes])[0].values
    return AuditEmbedding(vector=list(embedding), model_name="text-embedding-004")
