# [LATER-STEP] ocr_embedding.py

import openai
from document_client import DocumentClient
from document_models import OCRRequest, normalize_ocr_response


def embed_document_sections(image_path: str, section_count: int = 5) -> List[str]:
    """Embed OCR-extracted text sections for semantic retrieval.

    Args:
        image_path: Path to the scanned image.
        section_count: How many top-level sections to create.

    Returns:
        List of embedding strings (one per section).
    """
    client = DocumentClient()
    raw_text = client.extract_text(image_path)
    lines = normalize_ocr_response(raw_text)
    # Split into roughly equal sections
    n = len(lines)
    chunk_size = max(1, n // section_count)
    sections = ["\\n".join(lines[i : i + chunk_size]) for i in range(0, n, chunk_size)]
    embeddings = []
    for sec in sections:
        emb = openai.Embedding.create(model="text-embedding-3-large", input=sec)
        embeddings.append(emb.data[0].embedding)
    return embeddings
