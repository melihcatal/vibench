from document_client import extract_textract_blocks


def extract_key_values(payload, config=None):
    config = config or {}
    blocks, response = extract_textract_blocks(payload["document_bytes"], region=config.get("region"))
    key_values = []
    current_key = None
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            current_key = block.get("Text", "")
        elif block.get("BlockType") == "KEY_VALUE_SET" and "VALUE" in block.get("EntityTypes", []) and current_key:
            key_values.append({"key": current_key, "value": block.get("Text", "")})
            current_key = None
    return {"key_values": key_values, "raw": response}
