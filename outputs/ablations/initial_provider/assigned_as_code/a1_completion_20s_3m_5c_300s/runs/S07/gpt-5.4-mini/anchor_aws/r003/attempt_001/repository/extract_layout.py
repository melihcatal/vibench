from document_client import extract_textract_blocks


def extract_layout(payload, config=None):
    config = config or {}
    blocks, response = extract_textract_blocks(payload["document_bytes"], region=config.get("region"))
    layout = [
        {
            "block_type": block.get("BlockType"),
            "text": block.get("Text", ""),
            "page": block.get("Page"),
            "confidence": block.get("Confidence"),
        }
        for block in blocks
        if block.get("BlockType") in {"LINE", "WORD", "TABLE", "CELL", "KEY_VALUE_SET"}
    ]
    return {"layout": layout, "raw": response}
