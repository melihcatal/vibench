import os
from typing import Any, Dict, List, Optional

from google.cloud import documentai


def _text_from_anchor(document_text: str, text_anchor: Any) -> str:
    if not text_anchor or not getattr(text_anchor, "text_segments", None):
        return ""
    segments = []
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index) if segment.start_index is not None else 0
        end_index = int(segment.end_index) if segment.end_index is not None else 0
        segments.append(document_text[start_index:end_index])
    return "".join(segments)


def _normalized_vertices(layout: Any) -> List[Dict[str, float]]:
    vertices = []
    for vertex in getattr(layout.bounding_poly, "normalized_vertices", []) or []:
        vertices.append({"x": float(vertex.x), "y": float(vertex.y)})
    return vertices


def _table_cells(rows: Any, document_text: str) -> List[List[Dict[str, Any]]]:
    extracted_rows: List[List[Dict[str, Any]]] = []
    for row in rows:
        cells: List[Dict[str, Any]] = []
        for cell in row.cells:
            cells.append(
                {
                    "text": _text_from_anchor(document_text, cell.layout.text_anchor),
                    "row_span": int(getattr(cell, "row_span", 1) or 1),
                    "col_span": int(getattr(cell, "col_span", 1) or 1),
                    "bounding_poly": _normalized_vertices(cell.layout),
                }
            )
        extracted_rows.append(cells)
    return extracted_rows


def extract_tables(
    document_path: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    if processor_id is None:
        processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID")
    if mime_type is None:
        mime_type = os.environ.get("DOCUMENT_AI_MIME_TYPE", "application/pdf")

    if not project_id or not processor_id:
        raise ValueError("project_id and processor_id are required")

    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    with open(document_path, "rb") as file:
        raw_document = documentai.RawDocument(content=file.read(), mime_type=mime_type)

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    tables = []
    for page in document.pages:
        for table in page.tables:
            header_rows = _table_cells(table.header_rows, document.text)
            body_rows = _table_cells(table.body_rows, document.text)
            tables.append(
                {
                    "page": page.page_number,
                    "bounding_poly": _normalized_vertices(table.layout),
                    "header_rows": header_rows,
                    "body_rows": body_rows,
                }
            )

    return {"tables": tables}


__all__ = ["extract_tables"]
