from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, guess_content_type, read_bytes
from document_models import OCRResult, TextSpan, normalize_text


def extract_text(document_path: str) -> OCRResult:
    client = get_document_intelligence_client()
    payload = read_bytes(document_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=AnalyzeDocumentRequest(bytes_source=payload),
        content_type=guess_content_type(document_path),
    )
    result = poller.result()

    spans = []
    page_summaries = []
    text_parts = []

    for page in result.pages or []:
        line_count = 0
        for line in page.lines or []:
            line_text = normalize_text(line.content)
            if line_text:
                text_parts.append(line_text)
                spans.append(
                    TextSpan(
                        text=line_text,
                        confidence=None,
                        page=page.page_number,
                    )
                )
                line_count += 1
        page_summaries.append(
            {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "line_count": line_count,
            }
        )

    return OCRResult(
        text="\n".join(text_parts),
        pages=page_summaries,
        spans=spans,
        provider="azure-ai-documentintelligence:prebuilt-read",
        raw=result,
    )
