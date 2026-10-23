from document_client import get_textract_client
from document_models import normalize_blocks


def document_field_extraction(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(Document={"Bytes": payload["document_bytes"]}, FeatureTypes=["FORMS"])
    blocks = normalize_blocks(response.get("Blocks", []))
    return {"fields": [block for block in blocks if block.get("blocktype") == "KEY_VALUE_SET"]}
