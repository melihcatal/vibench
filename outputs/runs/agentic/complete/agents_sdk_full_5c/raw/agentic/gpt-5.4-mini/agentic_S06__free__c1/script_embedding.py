from __future__ import annotations

from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingModel


MODEL_ID = "text-embedding-004"


def embed_script(text: str) -> List[float]:
    vertexai.init(project=None, location="us-central1")
    model = TextEmbeddingModel.from_pretrained(MODEL_ID)
    embeddings = model.get_embeddings([text])
    return list(embeddings[0].values)


if __name__ == "__main__":
    print(len(embed_script("Narration text for search indexing.")))
