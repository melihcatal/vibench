from document_client import textract_client
from document_models import normalize_blocks, collect_tables


def extract_tables(payload, config=None):
    client = textract_client(config)
    response = client.analyze_document(Document={"Bytes": payload["document_bytes"]}, FeatureTypes=["TABLES"])
    blocks = normalize_blocks(response)
    return {"tables": collect_tables(blocks)}
