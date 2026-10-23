"""
[SAME-SCENARIO] Extracts plain text from a scanned document image.

Provider: Google Document AI (google-cloud-documentai)
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model/Processor: Built-in OCR processor (e.g., 'projects/{project}/locations/{location}/processors/{processor_id}')
"""

from __future__ import annotations

import os
from typing import Optional, List

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document as documentai_types

from document_client import load_image_bytes, get_google_project_id
from document_models import OcrLine, OcrWord, OcrDocumentResult, normalize_plain_text


def extract_text_from_document(
    file_path: str,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> OcrDocumentResult:
    """
    Extract plain text from a scanned document image or PDF using
    Google Document AI OCR processor.

    Uses the google-cloud-documentai SDK with concrete Google Document AI
    service endpoint documentai.googleapis.com.
    """
    project_id = project_id or get_google_project_id()
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable or project_id argument is required"
        )

    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client_options = ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    raw_bytes = load_image_bytes(file_path)
    if mime_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "application/pdf" if ext == ".pdf" else "image/png"

    raw_document = documentai.RawDocument(
        content=raw_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    pages_text_blocks: List[str] = []
    all_lines: List[OcrLine] = []
    page_count = len(document.pages)

    for page in document.pages:
        page_text_segments: List[str] = []
        for block in page.paragraphs:
            block_text = _extract_text_from_element(block, document.text)
            page_text_segments.append(block_text)

        page_plain = " ".join(page_text_segments)
        pages_text_blocks.append(page_plain)

        for line in page.lines:
            line_text = _extract_text_from_element(line, document.text)
            words: List[OcrWord] = []
            for token in line.tokens:
                token_text = _extract_text_from_element(token, document.text)
                token_conf = 0.0
                if token.detected_languages:
                    token_conf = token.detected_languages[0].confidence
                words.append(OcrWord(text=token_text, confidence=token_conf))
            all_lines.append(
                OcrLine(text=line_text, words=words, confidence=1.0)
            )

    full_text = "\n\n".join(pages_text_blocks)
    cleaned_text = normalize_plain_text(full_text)

    return OcrDocumentResult(
        plain_text=cleaned_text,
        lines=all_lines,
        page_count=page_count,
        language="en",
    )


def _extract_text_from_element(
    element: documentai_types.Document.Page.DetectedBreak,
    full_text: str,
) -> str:
    """Extract text from a layout element using layout token offsets."""
    if element.layout and element.layout.text_anchor and element.layout.text_anchor.text_segments:
        start_index = int(element.layout.text_anchor.text_segments[0].start_index)
        end_index = int(element.layout.text_anchor.text_segments[0].end_index)
        return full_text[start_index:end_index].strip()
    return ""
