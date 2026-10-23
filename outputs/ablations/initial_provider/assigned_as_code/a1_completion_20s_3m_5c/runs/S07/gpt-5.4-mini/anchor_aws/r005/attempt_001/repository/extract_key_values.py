from document_client import textract_client
from document_models import normalize_blocks, collect_kv_pairs


def extract_key_values(payload, config=None):
    client = textract_client(config)
    response = client.analyze_document(Document={"Bytes": payload["document_bytes"]}, FeatureTypes=["FORMS"])
    blocks = normalize_blocks(response)
    return {"key_values": collect_kv_pairs(blocks)}
