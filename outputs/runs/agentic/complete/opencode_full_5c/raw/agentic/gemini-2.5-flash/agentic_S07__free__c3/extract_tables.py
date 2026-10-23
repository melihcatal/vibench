import os
from typing import Union

from google.cloud import documentai_v1 as documentai

from document_client import GoogleCloudClients
from document_models import ExtractedTables, ExtractedTable, TableCell, BoundingPoly


def _convert_bounding_poly(document_proto_bounding_poly) -> BoundingPoly:
    if not document_proto_bounding_poly:
        return BoundingPoly(vertices=[])
    vertices = []
    for vertex in document_proto_bounding_poly.vertices:
        vertices.append({"x": vertex.x, "y": vertex.y})
    return BoundingPoly(vertices=vertices)


def extract_tables_from_document(
    document_bytes: bytes, mime_type: str
) -> ExtractedTables:
    """Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        document_bytes: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., 'application/pdf', 'image/tiff').

    Returns:
        An ExtractedTables object containing a list of extracted tables.
    """
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    location = os.environ.get("GOOGLE_LOCATION")
    # Using a general form parser processor for table extraction
    processor_id = os.environ.get(
        "DOCUMENT_AI_PROCESSOR_ID", "YOUR_FORM_PARSER_PROCESSOR_ID"
    )  # Replace with your processor ID

    if not project_id or not location or not processor_id:
        raise ValueError(
            "GOOGLE_PROJECT_ID, GOOGLE_LOCATION, and DOCUMENT_AI_PROCESSOR_ID environment variables must be set."
        )

    client = GoogleCloudClients.get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_tables: list[ExtractedTable] = []

    for page in document.pages:
        for table_proto in page.tables:
            cells: list[TableCell] = []
            for row_index, row in enumerate(table_proto.body_rows):
                for cell_proto in row.cells:
                    text_content = document.text[
                        cell_proto.layout.text_anchor.text_segments[
                            0
                        ].start_index : cell_proto.layout.text_anchor.text_segments[
                            0
                        ].end_index
                    ]
                    cells.append(
                        TableCell(
                            text_content=text_content,
                            bounding_box=_convert_bounding_poly(
                                cell_proto.layout.bounding_poly
                            ),
                            row_index=cell_proto.row_index,
                            column_index=cell_proto.col_index,
                            row_span=cell_proto.row_span,
                            column_span=cell_proto.col_span,
                        )
                    )

            # Extract header cells as well if present
            for row_index, row in enumerate(table_proto.header_rows):
                for cell_proto in row.cells:
                    text_content = document.text[
                        cell_proto.layout.text_anchor.text_segments[
                            0
                        ].start_index : cell_proto.layout.text_anchor.text_segments[
                            0
                        ].end_index
                    ]
                    cells.append(
                        TableCell(
                            text_content=text_content,
                            bounding_box=_convert_bounding_poly(
                                cell_proto.layout.bounding_poly
                            ),
                            row_index=cell_proto.row_index,  # Header row index can be distinct or negative depending on interpretation
                            column_index=cell_proto.col_index,
                            row_span=cell_proto.row_span,
                            column_span=cell_proto.col_span,
                        )
                    )

            table_text_content = (
                document.text[
                    table_proto.layout.text_anchor.text_segments[
                        0
                    ].start_index : table_proto.layout.text_anchor.text_segments[
                        0
                    ].end_index
                ]
                if table_proto.layout.text_anchor.text_segments
                else ""
            )

            extracted_tables.append(
                ExtractedTable(
                    cells=cells,
                    num_rows=len(table_proto.body_rows) + len(table_proto.header_rows),
                    num_columns=max([c.column_index + c.column_span for c in cells])
                    if cells
                    else 0,  # Simple way to get num_columns
                    bounding_box=_convert_bounding_poly(
                        table_proto.layout.bounding_poly
                    ),
                    text_content=table_text_content,
                )
            )

    return ExtractedTables(tables=extracted_tables)
