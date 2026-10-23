from __future__ import annotations

from typing import List

from google.cloud import documentai

from document_client import DocumentAiConfig, build_document_ai_client, build_process_request
from document_models import TableCell, TableResponse, normalize_document_ai_text


def extract_tables(image_bytes: bytes, mime_type: str = "image/png") -> TableResponse:
    config = DocumentAiConfig()
    client = build_document_ai_client(config.endpoint)
    request = build_process_request(image_bytes, mime_type=mime_type, config=config)
    response = client.process_document(request=request)
    document = response.document
    cells: List[TableCell] = []
    rows: List[List[str]] = []
    for page in document.pages:
        for table in getattr(page, "tables", []):
            for row_idx, row in enumerate(table.header_rows + table.body_rows):
                row_values: List[str] = []
                for col_idx, cell in enumerate(row.cells):
                    text = normalize_document_ai_text(documentai.Document.TextAnchor.get_text(cell.layout.text_anchor, document.text))
                    cells.append(TableCell(row_index=row_idx, column_index=col_idx, text=text, confidence=float(cell.layout.confidence or 0.0)))
                    row_values.append(text)
                rows.append(row_values)
    return TableResponse(cells=cells, rows=rows, raw={"provider": "google_document_ai"})
