from __future__ import annotations

from typing import List, Optional

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from model_client import init_vertex



def platform_output_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT", model_name: Optional[str] = None) -> List[float]:
    init_vertex()
    embedding_model = TextEmbeddingModel.from_pretrained(model_name or "text-embedding-005")
    response = embedding_model.get_embeddings([TextEmbeddingInput(text=text, task_type=task_type)])[0]
    return list(response.values)
