from document_client import get_client, open_document
from document_models import KeyValuePair, normalize_text


def extract_key_values(source: str):
    client = get_client()
    doc = open_document(source)
    if hasattr(doc, "read"):
        poller = client.begin_analyze_document("prebuilt-document", doc)
    else:
        poller = client.begin_analyze_document_from_url("prebuilt-document", doc)
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pairs.append(
            KeyValuePair(
                key=normalize_text(getattr(getattr(kv, "key", None), "content", "")),
                value=normalize_text(
                    getattr(getattr(kv, "value", None), "content", "")
                ),
                raw=kv,
            )
        )
    return pairs
