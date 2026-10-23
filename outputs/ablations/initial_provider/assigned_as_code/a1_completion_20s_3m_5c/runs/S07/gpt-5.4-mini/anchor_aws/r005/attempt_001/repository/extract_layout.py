from document_client import textract_client
from document_models import normalize_blocks


def extract_layout(payload, config=None):
    client = textract_client(config)
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["LAYOUT", "TABLES", "FORMS"],
    )
    return {"layout": normalize_blocks(response)}
