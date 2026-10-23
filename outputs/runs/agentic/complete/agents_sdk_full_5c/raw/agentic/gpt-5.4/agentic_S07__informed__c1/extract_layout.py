from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_LAYOUT_MODEL, get_document_intelligence_client, load_document_bytes
from document_models import polygon_to_dicts


def extract_layout(document_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_LAYOUT_MODEL,
        body=load_document_bytes(document_path),
    )
    result = poller.result()

    elements: List[Dict[str, Any]] = []
    for page in result.pages or []:
        for line in page.lines or []:
            elements.append({
                "kind": "line",
                "content": line.content,
                "page_number": page.page_number,
                "polygon": polygon_to_dicts(line.polygon),
            })
        for word in page.words or []:
            elements.append({
                "kind": "word",
                "content": word.content,
                "page_number": page.page_number,
                "polygon": polygon_to_dicts(word.polygon),
                "confidence": getattr(word, "confidence", None),
            })

    for table_index, table in enumerate(result.tables or []):
        for cell in table.cells or []:
            elements.append({
                "kind": "table_cell",
                "content": cell.content,
                "page_number": (cell.bounding_regions[0].page_number if cell.bounding_regions else None),
                "polygon": polygon_to_dicts(cell.bounding_regions[0].polygon if cell.bounding_regions else None),
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "table_index": table_index,
            })

    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "elements": elements,
    }
