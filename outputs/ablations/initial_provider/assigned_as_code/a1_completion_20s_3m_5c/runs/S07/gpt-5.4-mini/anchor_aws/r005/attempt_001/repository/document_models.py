def document_bytes(payload):
    if isinstance(payload, dict):
        return payload.get("document_bytes") or payload.get("bytes") or payload.get("content")
    return payload


def normalize_blocks(response):
    blocks = response.get("Blocks", [])
    normalized = []
    for block in blocks:
        normalized.append(
            {
                "id": block.get("Id"),
                "type": block.get("BlockType"),
                "text": block.get("Text"),
                "confidence": block.get("Confidence"),
                "row": block.get("RowIndex"),
                "column": block.get("ColumnIndex"),
                "row_span": block.get("RowSpan"),
                "column_span": block.get("ColumnSpan"),
                "entity_types": block.get("EntityTypes", []),
                "relationships": block.get("Relationships", []),
            }
        )
    return normalized


def collect_text_lines(blocks):
    return [block["text"] for block in blocks if block.get("type") == "LINE" and block.get("text")]


def collect_tables(blocks):
    tables = []
    current = None
    for block in blocks:
        if block.get("type") == "TABLE":
            current = {"id": block.get("id"), "cells": []}
            tables.append(current)
        elif block.get("type") == "CELL" and current is not None:
            current["cells"].append(block)
    return tables


def collect_kv_pairs(blocks):
    pairs = []
    for block in blocks:
        if block.get("type") == "KEY_VALUE_SET" and "KEY" in (block.get("entity_types") or []):
            pairs.append({"key": block.get("text"), "value": None, "id": block.get("id")})
    return pairs
