from document_client import get_textract_client


def extract_key_values(payload, config=None):
    client = get_textract_client(config)
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["FORMS"],
    )
    blocks = response.get("Blocks", [])
    key_map = {}
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            key = block.get("Text", "")
            value = block.get("Value", "")
            key_map[key] = value
    return {"key_values": key_map}
