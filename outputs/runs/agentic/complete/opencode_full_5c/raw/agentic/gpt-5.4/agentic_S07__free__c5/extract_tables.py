from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import DocumentInput, TableCell, TableResult, get_text_anchor_text


def extract_tables(document_input: DocumentInput) -> List[TableResult]:
    payload = {
        "skipHumanReview": True,
        "rawDocument": document_input.as_google_document()
        if document_input.bytes_base64
        else None,
        "gcsDocument": document_input.as_google_document()
        if document_input.source_uri
        else None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = process_document(payload)
    document = response.get("document", {})
    results: List[TableResult] = []
    for page_index, page in enumerate(document.get("pages", []), start=1):
        for table in page.get("tables", []):
            headers = []
            rows = []
            cells: List[TableCell] = []
            for header_row in table.get("headerRows", []):
                header_values = []
                for cell_index, cell in enumerate(header_row.get("cells", [])):
                    text = get_text_anchor_text(
                        document, cell.get("layout", {}).get("textAnchor")
                    )
                    header_values.append(text)
                    cells.append(
                        TableCell(
                            row_index=0,
                            column_index=cell_index,
                            text=text,
                            row_span=int(cell.get("rowSpan", 1)),
                            column_span=int(cell.get("colSpan", 1)),
                        )
                    )
                headers.extend(header_values)
            for row_index, body_row in enumerate(table.get("bodyRows", []), start=1):
                row_values = []
                for cell_index, cell in enumerate(body_row.get("cells", [])):
                    text = get_text_anchor_text(
                        document, cell.get("layout", {}).get("textAnchor")
                    )
                    row_values.append(text)
                    cells.append(
                        TableCell(
                            row_index=row_index,
                            column_index=cell_index,
                            text=text,
                            row_span=int(cell.get("rowSpan", 1)),
                            column_span=int(cell.get("colSpan", 1)),
                        )
                    )
                rows.append(row_values)
            results.append(
                TableResult(page=page_index, headers=headers, rows=rows, cells=cells)
            )
    return results
