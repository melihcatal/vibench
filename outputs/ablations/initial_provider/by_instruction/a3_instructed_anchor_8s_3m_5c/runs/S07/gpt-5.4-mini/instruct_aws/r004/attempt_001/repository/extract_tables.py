from typing import Any, Dict, List

from document_client import get_textract_client
from extract_text import _ensure_bytes


def extract_tables(document: Any) -> Dict[str, Any]:
    document_bytes = _ensure_bytes(document)
    client = get_textract_client()
    response = client.analyze_document(Document={"Bytes": document_bytes}, FeatureTypes=["TABLES"])
    blocks = response.get("Blocks", [])
    tables: List[Dict[str, Any]] = [block for block in blocks if block.get("BlockType") == "TABLE"]
    cells: List[Dict[str, Any]] = [block for block in blocks if block.get("BlockType") == "CELL"]
    return {"tables": tables, "cells": cells, "blocks": blocks}
