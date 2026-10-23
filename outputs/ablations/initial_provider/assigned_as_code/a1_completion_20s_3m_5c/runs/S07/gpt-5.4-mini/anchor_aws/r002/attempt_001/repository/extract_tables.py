from document_client import get_textract_client


def extract_tables(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["TABLES"],
    )
    blocks = response.get("Blocks", [])
    return {"tables": [b for b in blocks if b.get("BlockType") == "TABLE"]}
