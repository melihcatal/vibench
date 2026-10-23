from document_client import textract_client
from document_models import normalize_bytes


def extract_layout(payload, config=None):
    client = textract_client(config)
    response = client.analyze_document(Document={"Bytes": normalize_bytes(payload)}, FeatureTypes=["LAYOUT"])
    return {"blocks": response.get("Blocks", [])}
