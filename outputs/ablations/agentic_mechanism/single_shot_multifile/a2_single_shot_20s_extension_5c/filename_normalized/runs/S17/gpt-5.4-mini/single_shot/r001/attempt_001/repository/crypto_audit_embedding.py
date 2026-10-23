from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import aiplatform


def crypto_audit_embedding(text: str) -> Dict[str, Any]:
    aiplatform.init(project=None, location="us-central1")
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embedding = model.get_embeddings([text])[0].values
    return {"provider": "google-cloud-aiplatform", "model": "textembedding-gecko@003", "embedding": list(embedding)}
