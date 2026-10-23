from __future__ import annotations

from typing import List, Optional

from document_client import load_document_input, textract_bytes_payload, textract_client
from document_models import KeyValuePair, normalize_key_values


def extract_key_values(image_path: Optional[str] = None, content: Optional[bytes] = None, mime_type: str = "image/png") -> List[KeyValuePair]:
    document = load_document_input(content=content, path=image_path, mime_type=mime_type)
    client = textract_client()
    response = client.analyze_document(Document=textract_bytes_payload(document), FeatureTypes=["FORMS"])
    block_map = {block.get("Id"): block for block in response.get("Blocks", []) if block.get("Id")}
    pairs = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") != "KEY_VALUE_SET" or "KEY" not in block.get("EntityTypes", []):
            continue
        key_text = []
        value_text = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for child_id in rel.get("Ids", []):
                    child = block_map.get(child_id)
                    if child and child.get("Text"):
                        key_text.append(child.get("Text", ""))
            if rel.get("Type") == "VALUE":
                for value_id in rel.get("Ids", []):
                    value_block = block_map.get(value_id)
                    if value_block:
                        for rel2 in value_block.get("Relationships", []):
                            if rel2.get("Type") == "CHILD":
                                for child_id in rel2.get("Ids", []):
                                    child = block_map.get(child_id)
                                    if child and child.get("Text"):
                                        value_text.append(child.get("Text", ""))
        pairs.append({"key": " ".join(key_text).strip(), "value": " ".join(value_text).strip(), "confidence": block.get("Confidence"), "raw": block})
    return normalize_key_values(pairs)
