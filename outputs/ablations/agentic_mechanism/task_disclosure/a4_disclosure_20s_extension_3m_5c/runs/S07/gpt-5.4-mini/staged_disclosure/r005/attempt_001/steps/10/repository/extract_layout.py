import os
from typing import Any, Dict, List, Optional

from google.cloud import documentai


def extract_layout(
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

    def normalized_vertices(layout: Any) -> List[Dict[str, float]]:
        vertices = []
        for vertex in layout.bounding_poly.normalized_vertices:
            vertices.append({"x": float(vertex.x), "y": float(vertex.y)})
        return vertices

    blocks = []
    for page in document.pages:
        for block in page.blocks:
            blocks.append(
                {
                    "page": page.page_number,
                    "text": document.text[block.layout.text_anchor.text_segments[0].start_index:block.layout.text_anchor.text_segments[0].end_index]
                    if block.layout.text_anchor and block.layout.text_anchor.text_segments
                    else "",
                    "bounding_poly": normalized_vertices(block.layout),
                }
            )

    lines = []
    for page in document.pages:
        for line in page.lines:
            lines.append(
                {
                    "page": page.page_number,
                    "text": document.text[line.layout.text_anchor.text_segments[0].start_index:line.layout.text_anchor.text_segments[0].end_index]
                    if line.layout.text_anchor and line.layout.text_anchor.text_segments
                    else "",
                    "bounding_poly": normalized_vertices(line.layout),
                }
            )

    tables = []
    for page in document.pages:
        for table in page.tables:
            tables.append(
                {
                    "page": page.page_number,
                    "bounding_poly": normalized_vertices(table.layout),
                    "header_rows": len(table.header_rows),
                    "body_rows": len(table.body_rows),
                }
            )

    return {"blocks": blocks, "lines": lines, "tables": tables}


__all__ = ["extract_layout"]
