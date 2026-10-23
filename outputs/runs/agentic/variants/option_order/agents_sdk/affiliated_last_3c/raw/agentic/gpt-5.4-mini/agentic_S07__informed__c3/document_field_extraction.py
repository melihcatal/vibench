from __future__ import annotations

from typing import Dict, Optional

from document_client import get_textract_client


def extract_structured_fields(image_bytes: bytes, mime_type: str = "image/png", region_name: Optional[str] = None) -> Dict[str, str]:
    helper = get_textract_client(region_name=region_name)
    response = helper.client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["FORMS"],
    )
    result: Dict[str, str] = {}
    blocks = response.get("Blocks", [])
    block_map = {b.get("Id"): b for b in blocks if b.get("Id")}
    for block in blocks:
        if block.get("BlockType") != "KEY_VALUE_SET" or "KEY" not in block.get("EntityTypes", []):
            continue
        key = []
        value = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for cid in rel.get("Ids", []):
                    child = block_map.get(cid, {})
                    if child.get("BlockType") == "WORD":
                        key.append(child.get("Text", ""))
            if rel.get("Type") == "VALUE":
                for vid in rel.get("Ids", []):
                    val = block_map.get(vid, {})
                    for vrel in val.get("Relationships", []):
                        if vrel.get("Type") == "CHILD":
                            for wid in vrel.get("Ids", []):
                                word = block_map.get(wid, {})
                                if word.get("BlockType") == "WORD":
                                    value.append(word.get("Text", ""))
        key_text = " ".join(key).strip()
        if key_text:
            result[key_text] = " ".join(value).strip()
    return result
