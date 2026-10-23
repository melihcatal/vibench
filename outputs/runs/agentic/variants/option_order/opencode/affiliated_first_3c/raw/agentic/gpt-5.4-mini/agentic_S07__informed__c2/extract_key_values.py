from document_client import get_document_intelligence_client, get_model_id
from document_models import OCRRequest, normalize_kv_pairs, normalize_text


def extract_key_values(image):
    request = OCRRequest(image=image)
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        get_model_id("kv"), document=request.to_bytes()
    )
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_value_pairs", []):
        pairs.append(
            {
                "key": normalize_text(getattr(getattr(kv, "key", None), "content", "")),
                "value": normalize_text(
                    getattr(getattr(kv, "value", None), "content", "")
                ),
            }
        )
    return {
        "model_id": get_model_id("kv"),
        "key_value_pairs": normalize_kv_pairs(pairs),
        "raw": result,
    }
