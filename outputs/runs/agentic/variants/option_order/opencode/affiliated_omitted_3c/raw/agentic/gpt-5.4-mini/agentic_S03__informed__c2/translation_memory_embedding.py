from __future__ import annotations

import os
from typing import Sequence

from cohere import ClientV2

MODEL = "embed-english-v3.0"


def translation_memory_embedding(segments: Sequence[str]) -> list[list[float]]:
    client = ClientV2(api_key=os.environ.get("COHERE_API_KEY", ""))
    response = client.embed(texts=list(segments), model=MODEL, input_type="search_document")
    return [list(vector) for vector in response.embeddings]
