from __future__ import annotations

from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, load_config
from document_models import DocumentInput, KeyValueResult


def extract_key_values(document: DocumentInput, model_id: Optional[str] = None) -> KeyValueResult:
    cfg = load_config(model_id=model_id or document.model or "prebuilt-document", locale=document.locale)
    client = build_client(cfg)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document.content),
        content_type=document.content_type,
        locale=cfg.locale,
    )
    result = poller.result()
    key_values = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", None)
        value = getattr(getattr(kv, "value", None), "content", None)
        key_values.append({"key": key, "value": value, "confidence": getattr(kv, "confidence", None)})
    return KeyValueResult(key_values=key_values, raw=result)
