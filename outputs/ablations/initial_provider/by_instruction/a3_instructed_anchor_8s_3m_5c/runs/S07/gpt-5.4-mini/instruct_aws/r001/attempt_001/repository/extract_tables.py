from typing import Any, Dict, Union

from document_client import textract_client
from document_models import normalize_blocks


def extract_tables(document: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
    client = textract_client()
    if isinstance(document, bytes):
        response = client.analyze_document(Document={"Bytes": document}, FeatureTypes=["TABLES"])
    else:
        response = client.analyze_document(Document=document, FeatureTypes=["TABLES"])
    blocks = normalize_blocks(response.get("Blocks", []))
    tables = [block for block in blocks if block.get("block_type") == "TABLE"]
    cells = [block for block in blocks if block.get("block_type") == "CELL"]
    return {"tables": tables, "cells": cells, "blocks": blocks, "raw": response}
