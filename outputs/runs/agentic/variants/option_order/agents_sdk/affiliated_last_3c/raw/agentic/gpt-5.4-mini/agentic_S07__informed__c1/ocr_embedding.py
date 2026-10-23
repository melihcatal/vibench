from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from document_models import OCRResponse


def embed_document_sections(response: OCRResponse, sections: List[str] | None = None) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts = sections or [response.text]
    result = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in result.data]
