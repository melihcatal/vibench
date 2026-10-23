import os
from typing import List, Optional, Dict, Any
import openai
from document_models import DocumentTextResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_document_sections(
    ocr_result: DocumentTextResult,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    model_name = model or OPENAI_EMBEDDING_MODEL

    client = openai.OpenAI(api_key=api_key)

    sections = []
    if ocr_result.lines:
        for line in ocr_result.lines:
            if line.text.strip():
                sections.append(
                    {
                        "text": line.text,
                        "section_type": "line",
                    }
                )
    elif ocr_result.raw_text.strip():
        sections.append(
            {
                "text": ocr_result.raw_text,
                "section_type": "full_document",
            }
        )

    if not sections:
        return []

    embeddings = []
    for section in sections:
        response = client.embeddings.create(
            input=section["text"],
            model=model_name,
        )
        embedding_data = response.data[0].embedding
        embeddings.append(
            {
                "text": section["text"],
                "section_type": section["section_type"],
                "embedding": embedding_data,
                "model": model_name,
            }
        )

    return embeddings


def embed_texts(
    texts: List[str],
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    model_name = model or OPENAI_EMBEDDING_MODEL

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=texts,
        model=model_name,
    )

    results = []
    for idx, item in enumerate(response.data):
        results.append(
            {
                "text": texts[idx],
                "embedding": item.embedding,
                "model": model_name,
            }
        )

    return results


if __name__ == "__main__":
    sample_result = DocumentTextResult(
        raw_text="Sample document text for embedding.",
        lines=[],
        confidence=1.0,
    )
    embeddings = embed_document_sections(sample_result)
    for emb in embeddings:
        print(f"Section: {emb['text'][:50]}... Model: {emb['model']}")
