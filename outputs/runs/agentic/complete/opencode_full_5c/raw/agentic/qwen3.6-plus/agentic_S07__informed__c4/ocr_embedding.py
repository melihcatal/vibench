import os
from typing import List, Dict, Any
from openai import OpenAI
from document_models import OcrResult


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[float]:
    client = get_openai_client()
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def embed_texts(
    texts: List[str], model: str = OPENAI_EMBEDDING_MODEL
) -> List[List[float]]:
    client = get_openai_client()
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


def embed_ocr_sections(
    result: OcrResult, model: str = OPENAI_EMBEDDING_MODEL
) -> List[Dict[str, Any]]:
    client = get_openai_client()
    sections = []

    if result.full_text:
        sections.append(
            {
                "section_type": "full_document",
                "text": result.full_text,
                "embedding": embed_text(result.full_text, model),
            }
        )

    for idx, seg in enumerate(result.segments):
        if seg.text:
            sections.append(
                {
                    "section_type": "text_segment",
                    "text": seg.text,
                    "confidence": seg.confidence,
                    "embedding": embed_text(seg.text, model),
                }
            )

    for elem in result.layout_elements:
        if elem.text:
            sections.append(
                {
                    "section_type": elem.element_type,
                    "text": elem.text,
                    "confidence": elem.confidence,
                    "bounding_box": elem.bounding_box,
                    "embedding": embed_text(elem.text, model),
                }
            )

    for table in result.tables:
        table_text = " ".join(cell.text for cell in table.cells if cell.text)
        if table_text:
            sections.append(
                {
                    "section_type": "table",
                    "text": table_text,
                    "num_rows": table.num_rows,
                    "num_cols": table.num_cols,
                    "embedding": embed_text(table_text, model),
                }
            )

    for kv in result.key_values:
        kv_text = f"{kv.key}: {kv.value}"
        if kv_text.strip():
            sections.append(
                {
                    "section_type": "key_value",
                    "text": kv_text,
                    "key": kv.key,
                    "value": kv.value,
                    "embedding": embed_text(kv_text, model),
                }
            )

    return sections


def embed_document_sections(
    file_bytes: bytes, mime_type: str = "image/png", model: str = OPENAI_EMBEDDING_MODEL
) -> List[Dict[str, Any]]:
    from extract_text import extract_text_from_image

    ocr_result = extract_text_from_image(file_bytes, mime_type)
    return embed_ocr_sections(ocr_result, model)
