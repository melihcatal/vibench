from __future__ import annotations

from typing import List, Optional

from document_client import get_textract_client
from document_models import KeyValuePair, normalize_pairs


def extract_key_values(image_bytes: bytes, mime_type: str = "image/png", region_name: Optional[str] = None) -> List[KeyValuePair]:
    helper = get_textract_client(region_name=region_name)
    response = helper.client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["FORMS"],
    )
    blocks = response.get("Blocks", [])
    block_map = {b.get("Id"): b for b in blocks if b.get("Id")}
    pairs: List[KeyValuePair] = []
    for block in blocks:
        if block.get("BlockType") != "KEY_VALUE_SET" or "KEY" not in block.get("EntityTypes", []):
            continue
        key_text = []
        value_text = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") != "CHILD":
                continue
            for cid in rel.get("Ids", []):
                child = block_map.get(cid, {})
                if child.get("BlockType") == "WORD":
                    key_text.append(child.get("Text", ""))
            if rel.get("Type") == "VALUE":
                for vid in rel.get("Ids", []):
                    value_block = block_map.get(vid, {})
                    for vrel in value_block.get("Relationships", []):
                        if vrel.get("Type") == "CHILD":
                            for wid in vrel.get("Ids", []):
                                word = block_map.get(wid, {})
                                if word.get("BlockType") == "WORD":
                                    value_text.append(word.get("Text", ""))
        pairs.append(KeyValuePair(key=" ".join(key_text), value=" ".join(value_text), confidence=block.get("Confidence")))
    return normalize_pairs(pairs)
