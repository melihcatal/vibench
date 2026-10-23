from dataclasses import dataclass
from typing import Any


@dataclass
class DocumentTextRequest:
    image_bytes: bytes


@dataclass
class DocumentLayoutRequest:
    image_bytes: bytes


@dataclass
class DocumentTableRequest:
    image_bytes: bytes


@dataclass
class DocumentKeyValueRequest:
    image_bytes: bytes


def normalize_text_from_blocks(blocks: list[dict[str, Any]]) -> str:
    lines = []
    for block in blocks:
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return "\n".join(lines)


def extract_blocks(response: dict[str, Any]) -> list[dict[str, Any]]:
    return response.get("Blocks", [])


def normalize_kv_pairs(blocks: list[dict[str, Any]]) -> dict[str, str]:
    block_map = {block["Id"]: block for block in blocks if "Id" in block}
    kv = {}
    for block in blocks:
        if block.get("BlockType") != "KEY_VALUE_SET" or "KEY" not in block.get(
            "EntityTypes", []
        ):
            continue
        key_text = []
        value_text = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for cid in rel.get("Ids", []):
                    child = block_map.get(cid, {})
                    if child.get("Text"):
                        key_text.append(child["Text"])
            if rel.get("Type") == "VALUE":
                for vid in rel.get("Ids", []):
                    value_block = block_map.get(vid, {})
                    for vrel in value_block.get("Relationships", []):
                        if vrel.get("Type") == "CHILD":
                            for cid in vrel.get("Ids", []):
                                child = block_map.get(cid, {})
                                if child.get("Text"):
                                    value_text.append(child["Text"])
        if key_text:
            kv[" ".join(key_text)] = " ".join(value_text)
    return kv
