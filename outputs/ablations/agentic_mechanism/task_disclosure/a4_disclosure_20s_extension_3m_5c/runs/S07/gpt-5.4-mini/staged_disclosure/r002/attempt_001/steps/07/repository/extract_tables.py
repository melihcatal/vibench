import json
import os
import sys
from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def _normalize_table(table: Any) -> Dict[str, Any]:
    cells: List[Dict[str, Any]] = []
    for cell in getattr(table, "cells", []) or []:
        cells.append(
            {
                "row_index": getattr(cell, "row_index", None),
                "column_index": getattr(cell, "column_index", None),
                "row_span": getattr(cell, "row_span", 1),
                "column_span": getattr(cell, "column_span", 1),
                "content": getattr(cell, "content", ""),
                "kind": getattr(cell, "kind", None),
            }
        )
    return {
        "row_count": getattr(table, "row_count", None),
        "column_count": getattr(table, "column_count", None),
        "cells": cells,
    }


def extract_tables(document_path: str) -> List[Dict[str, Any]]:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    api_key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_API_KEY"]
    model_id = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout")

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(model_id=model_id, body=f)
        result = poller.result()

    tables = []
    for table in getattr(result, "tables", []) or []:
        tables.append(_normalize_table(table))
    return tables


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_tables.py DOCUMENT_PATH")
    output = extract_tables(sys.argv[1])
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
