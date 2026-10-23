import os
from openai import OpenAI
from document_models import EmbeddingResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_document_sections(
    sections: list[str],
    model: str = EMBEDDING_MODEL,
) -> EmbeddingResult:
    if not sections:
        return EmbeddingResult(sections=[], model=model)

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        input=sections,
        model=model,
    )

    embeddings = []
    for item in sorted(response.data, key=lambda x: x.index):
        embeddings.append(item.embedding)

    return EmbeddingResult(
        embeddings=embeddings,
        sections=sections,
        model=model,
    )


def embed_single_section(
    text: str,
    model: str = EMBEDDING_MODEL,
) -> list[float]:
    if not text.strip():
        return []

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    return response.data[0].embedding


def embed_ocr_result(
    ocr_text: str,
    chunk_size: int = 1000,
    model: str = EMBEDDING_MODEL,
) -> EmbeddingResult:
    if not ocr_text.strip():
        return EmbeddingResult(sections=[], model=model)

    sections = _split_text_into_sections(ocr_text, chunk_size)
    return embed_document_sections(sections, model=model)


def _split_text_into_sections(text: str, chunk_size: int) -> list[str]:
    paragraphs = text.split("\n\n")
    sections = []
    current_section = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_section) + len(para) + 2 <= chunk_size:
            if current_section:
                current_section += "\n\n" + para
            else:
                current_section = para
        else:
            if current_section:
                sections.append(current_section)
            current_section = para

    if current_section:
        sections.append(current_section)

    return sections
