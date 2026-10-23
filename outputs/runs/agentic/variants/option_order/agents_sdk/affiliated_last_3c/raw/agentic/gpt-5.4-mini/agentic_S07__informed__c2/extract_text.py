from __future__ import annotations

from typing import Optional

from document_client import DocumentServiceClient
from document_models import DocumentRequest, OCRTextResponse, normalize_whitespace


def extract_text(document_path: Optional[str] = None, document_bytes: Optional[bytes] = None, language_hint: Optional[str] = None) -> OCRTextResponse:
    request = DocumentRequest(document_path=document_path, document_bytes=document_bytes, language_hint=language_hint)
    client = DocumentServiceClient()
    result = client.analyze(request, model_id="prebuilt-read")
    lines = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            content = getattr(line, "content", "")
            if content:
                lines.append(content)
    text = normalize_whitespace("\n".join(lines))
    return OCRTextResponse(text=text, provider="azure-document-intelligence", metadata={"model_id": "prebuilt-read"})
