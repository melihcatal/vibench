from document_client import get_textract_client


def extract_layout(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["LAYOUT"],
    )
    blocks = response.get("Blocks", [])
    return {"blocks": [b for b in blocks if b.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_LIST", "LAYOUT_TABLE", "LAYOUT_KEY_VALUE"}]}
