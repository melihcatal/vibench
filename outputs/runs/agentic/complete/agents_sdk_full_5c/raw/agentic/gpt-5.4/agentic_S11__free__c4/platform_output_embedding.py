from __future__ import annotations

from typing import Dict, List, Optional

import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from model_client import get_project_id


DEFAULT_EMBEDDING_MODEL = "text-embedding-004"


def platform_output_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
    project_id: Optional[str] = None,
    location: str = "us-central1",
) -> Dict[str, object]:
    resolved_project = get_project_id(project_id)
    vertexai.init(project=resolved_project, location=location)
    model = TextEmbeddingModel.from_pretrained(DEFAULT_EMBEDDING_MODEL)
    embeddings = model.get_embeddings([TextEmbeddingInput(text=text, task_type=task_type)])
    vector: List[float] = embeddings[0].values
    return {
        "provider": "google_vertex_ai",
        "model": DEFAULT_EMBEDDING_MODEL,
        "task_type": task_type,
        "embedding": vector,
        "dimension": len(vector),
    }
