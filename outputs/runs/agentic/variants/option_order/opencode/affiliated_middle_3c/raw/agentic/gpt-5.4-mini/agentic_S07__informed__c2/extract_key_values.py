from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_endpoint, load_config, require_bytes
from document_models import KeyValueResult, normalize_pairs


def extract_key_values(document: bytes, mime_type: str = "image/png") -> KeyValueResult:
    config = load_config()
    client = DocumentIntelligenceClient(
        ensure_endpoint(config), AzureKeyCredential(config.api_key or "")
    )
    poller = client.begin_analyze_document(
        "prebuilt-document", require_bytes(document), content_type=mime_type
    )
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pairs.append(
            {
                "key": getattr(getattr(kv, "key", None), "content", ""),
                "value": getattr(getattr(kv, "value", None), "content", ""),
            }
        )
    return KeyValueResult(
        pairs=normalize_pairs(pairs),
        raw=result.as_dict() if hasattr(result, "as_dict") else None,
    )
