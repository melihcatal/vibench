from document_client import get_textract_client
from document_models import normalize_blocks


def extract_tables(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(Document={"Bytes": payload["document_bytes"]}, FeatureTypes=["TABLES"])
    return {"tables": [block for block in normalize_blocks(response.get("Blocks", [])) if block.get("blocktype") == "TABLE"]}
