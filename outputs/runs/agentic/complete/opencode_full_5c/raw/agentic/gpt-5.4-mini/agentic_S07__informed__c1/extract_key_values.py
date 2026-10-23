from document_client import textract_client
from document_models import DocumentKeyValueRequest, extract_blocks, normalize_kv_pairs


def extract_key_values(request: DocumentKeyValueRequest | bytes) -> dict[str, str]:
    image_bytes = (
        request.image_bytes if isinstance(request, DocumentKeyValueRequest) else request
    )
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    return normalize_kv_pairs(extract_blocks(response))
