from __future__ import annotations

from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, load_config
from document_models import DocumentInput, TextResult, normalize_text


def extract_text(document: DocumentInput, model_id: Optional[str] = None) -> TextResult:
    cfg = load_config(model_id=model_id or document.model or "prebuilt-read", locale=document.locale)
    client = build_client(cfg)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document.content),
        content_type=document.content_type,
        locale=cfg.locale,
    )
    result = poller.result()
    text = normalize_text(getattr(result, "content", None) or getattr(result, "text", None))
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append({"number": getattr(page, "page_number", None), "lines": getattr(page, "lines", None)})
    return TextResult(text=text, pages=pages, raw=result)
