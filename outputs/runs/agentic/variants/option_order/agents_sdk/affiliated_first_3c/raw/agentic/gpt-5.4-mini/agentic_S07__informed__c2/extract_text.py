from __future__ import annotations

from typing import Union

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_client, load_config
from document_models import DocumentInput, TextExtractionResult

PROVIDER = "azure-document-intelligence"
MODEL_ID = "prebuilt-read"


def extract_text(document: Union[DocumentInput, str]) -> TextExtractionResult:
    client = get_client()
    cfg = load_config()
    source_url = document.source_url if isinstance(document, DocumentInput) else str(document)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id if cfg.model_id else MODEL_ID,
        analyze_request=AnalyzeDocumentRequest(url_source=source_url),
    )
    result = poller.result()
    text = "\n".join((page.content or "") for page in result.pages) if getattr(result, "pages", None) else (getattr(result, "content", "") or "")
    pages = [page.page_number for page in getattr(result, "pages", []) if getattr(page, "page_number", None) is not None]
    return TextExtractionResult(text=text, pages=pages, provider=PROVIDER, model_id=cfg.model_id or MODEL_ID)
