from document_client import get_textract_client
from document_models import normalize_blocks


def extract_layout(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(Document={"Bytes": payload["document_bytes"]}, FeatureTypes=["LAYOUT"])
    return {"blocks": normalize_blocks(response.get("Blocks", []))}
