from typing import Any, Dict, List


def _blocks_by_type(response: Dict[str, Any], block_type: str) -> List[Dict[str, Any]]:
    return [block for block in response.get("Blocks", []) if block.get("BlockType") == block_type]


def normalize_ocr_text_result(response: Dict[str, Any], *, source: str) -> Dict[str, Any]:
    lines = [b.get("Text", "") for b in _blocks_by_type(response, "LINE") if b.get("Text")]
    return {"source": source, "text": "
".join(lines), "lines": lines, "raw": response}


def normalize_layout_result(response: Dict[str, Any], *, source: str) -> Dict[str, Any]:
    blocks = response.get("Blocks", [])
    return {"source": source, "blocks": blocks, "lines": _blocks_by_type(response, "LINE"), "tables": _blocks_by_type(response, "TABLE"), "raw": response}


def normalize_table_result(response: Dict[str, Any], *, source: str) -> Dict[str, Any]:
    cells = _blocks_by_type(response, "CELL")
    tables = _blocks_by_type(response, "TABLE")
    return {"source": source, "tables": tables, "cells": cells, "raw": response}


def normalize_key_value_result(response: Dict[str, Any], *, source: str) -> Dict[str, Any]:
    blocks = response.get("Blocks", [])
    kv_pairs = []
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET":
            kv_pairs.append(block)
    return {"source": source, "key_values": kv_pairs, "raw": response}
