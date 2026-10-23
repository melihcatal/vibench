from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import create_client
from document_models import KeyValueResult


def extract_key_values(
    content_bytes: bytes, mime_type: str = "image/png"
) -> KeyValueResult:
    client = create_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        analyze_request=AnalyzeDocumentRequest(bytes_source=content_bytes),
        content_type=mime_type,
    )
    result = poller.result()
    pairs = {}
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "")
        value = getattr(getattr(kv, "value", None), "content", "")
        if key:
            pairs[key] = value
    return KeyValueResult(pairs=pairs, raw={"result": result})
