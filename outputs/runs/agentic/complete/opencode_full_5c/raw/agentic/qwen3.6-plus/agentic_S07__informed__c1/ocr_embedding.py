import os
from openai import OpenAI
from document_models import OCRTextResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)


def embed_ocr_sections(ocr_response: OCRTextResponse, section_size: int = 500) -> dict:
    if not ocr_response or not ocr_response.text:
        return {"embeddings": [], "sections": [], "model": OPENAI_EMBEDDING_MODEL}

    api_key = OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    text = ocr_response.text
    sections = []
    for i in range(0, len(text), section_size):
        section = text[i : i + section_size]
        if section.strip():
            sections.append(section)

    embeddings = []
    for section in sections:
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=section,
        )
        embedding = response.data[0].embedding
        embeddings.append(
            {
                "text": section,
                "embedding": embedding,
                "dimension": len(embedding),
            }
        )

    return {
        "embeddings": [e["embedding"] for e in embeddings],
        "sections": [e["text"] for e in embeddings],
        "model": OPENAI_EMBEDDING_MODEL,
        "section_count": len(embeddings),
    }


def embed_text_sections(text: str, section_size: int = 500) -> dict:
    if not text:
        return {"embeddings": [], "sections": [], "model": OPENAI_EMBEDDING_MODEL}

    api_key = OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    sections = []
    for i in range(0, len(text), section_size):
        section = text[i : i + section_size]
        if section.strip():
            sections.append(section)

    embeddings = []
    for section in sections:
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=section,
        )
        embedding = response.data[0].embedding
        embeddings.append(
            {
                "text": section,
                "embedding": embedding,
                "dimension": len(embedding),
            }
        )

    return {
        "embeddings": [e["embedding"] for e in embeddings],
        "sections": [e["text"] for e in embeddings],
        "model": OPENAI_EMBEDDING_MODEL,
        "section_count": len(embeddings),
    }
