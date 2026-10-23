from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from document_client import get_document_client, AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
from document_models import (
    DocumentRequest,
    OcrResult,
    OcrLine,
    BoundingBox,
    normalize_confidence,
    normalize_bounding_box,
)

AZURE_OCR_MODEL_ID = "prebuilt-read"


def extract_text_from_document(
    request: DocumentRequest,
    client: DocumentIntelligenceClient | None = None,
    language: str = "en",
) -> OcrResult:
    if client is None:
        client = get_document_client()

    doc_bytes = request.read_bytes()

    poller = client.begin_analyze_document(
        model_id=AZURE_OCR_MODEL_ID,
        body={
            "base64Source": __import__("base64").b64encode(doc_bytes).decode("utf-8")
        },
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    all_text_parts: list[str] = []
    ocr_lines: list[OcrLine] = []

    for page_idx, page in enumerate(result.pages or []):
        page_lines = page.lines or []
        for line in page_lines:
            line_text = line.content or ""
            all_text_parts.append(line_text)

            confidence = normalize_confidence(line.confidence)
            bbox = normalize_bounding_box(line.polygon)

            words = []
            for word in line.words or []:
                words.append(
                    {
                        "text": word.content or "",
                        "confidence": normalize_confidence(word.confidence),
                    }
                )

            ocr_lines.append(
                OcrLine(
                    text=line_text,
                    confidence=confidence,
                    bounding_box=bbox,
                    words=words,
                )
            )

    full_text = "\n".join(all_text_parts)
    overall_confidence = (
        normalize_confidence(result.pages[0].confidence) if result.pages else 0.0
    )

    return OcrResult(
        text=full_text,
        lines=ocr_lines,
        confidence=overall_confidence,
        page_number=1,
        language=language,
    )


def extract_text_from_file(
    file_path: str,
    content_type: str = "application/pdf",
    language: str = "en",
) -> OcrResult:
    request = DocumentRequest.from_file(file_path, content_type)
    return extract_text_from_document(request, language=language)


def extract_text_from_url(
    url: str,
    language: str = "en",
    client: DocumentIntelligenceClient | None = None,
) -> OcrResult:
    if client is None:
        client = get_document_client()

    poller = client.begin_analyze_document(
        model_id=AZURE_OCR_MODEL_ID,
        body={"urlSource": url},
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    all_text_parts: list[str] = []
    ocr_lines: list[OcrLine] = []

    for page in result.pages or []:
        for line in page.lines or []:
            line_text = line.content or ""
            all_text_parts.append(line_text)
            ocr_lines.append(
                OcrLine(
                    text=line_text,
                    confidence=normalize_confidence(line.confidence),
                    bounding_box=normalize_bounding_box(line.polygon),
                )
            )

    full_text = "\n".join(all_text_parts)
    overall_confidence = (
        normalize_confidence(result.pages[0].confidence) if result.pages else 0.0
    )

    return OcrResult(
        text=full_text,
        lines=ocr_lines,
        confidence=overall_confidence,
        page_number=1,
        language=language,
    )
