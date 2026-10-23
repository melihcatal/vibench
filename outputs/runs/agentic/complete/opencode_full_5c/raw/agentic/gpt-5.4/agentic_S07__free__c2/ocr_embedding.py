from __future__ import annotations

from typing import Iterable, List

from document_client import get_default_embedding_model, get_openai_client


def embed_document_sections(sections: Iterable[str]) -> List[List[float]]:
    section_list = list(sections)
    client = get_openai_client()
    response = client.embeddings.create(
        model=get_default_embedding_model(),
        input=section_list,
    )
    return [item.embedding for item in response.data]
