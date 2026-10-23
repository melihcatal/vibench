from __future__ import annotations

from typing import Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, load_config
from document_models import DocumentInput, FieldsResult, normalize_text


def extract_document_fields(document: DocumentInput) -> FieldsResult:
    cfg = load_config(model_id=document.model or "prebuilt-document", locale=document.locale)
    client = build_client(cfg)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document.content),
        content_type=document.content_type,
        locale=cfg.locale,
    )
    result = poller.result()
    fields: Dict[str, str] = {}
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = normalize_text(getattr(getattr(kv, "key", None), "content", None))
        value = normalize_text(getattr(getattr(kv, "value", None), "content", None))
        if key:
            fields[key] = value
    return FieldsResult(fields=fields, raw=result)
