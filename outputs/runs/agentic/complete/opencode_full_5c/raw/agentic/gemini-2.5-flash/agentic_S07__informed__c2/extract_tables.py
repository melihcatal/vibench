import os
from typing import List

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_client import get_documentai_client
from document_models import ExtractedTable


def extract_tables_from_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> List[ExtractedTable]:
    """Extracts table cells and row structure from a document using Google Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the form parser processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A list of ExtractedTable objects.
    """
    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document
    extracted_tables: List[ExtractedTable] = []

    for page in document.pages:
        for table in page.tables:
            table_content = ""
            rows_data: List[List[str]] = []

            # Extract header rows
            header_row_data: List[str] = []
            for header_cell in table.header_rows[0].cells:
                text_segment = header_cell.layout.text_anchor.text_segments[0]
                header_row_data.append(
                    document.text[text_segment.start_index : text_segment.end_index]
                )
            if header_row_data:
                rows_data.append(header_row_data)

            # Extract body rows
            for body_row in table.body_rows:
                row_data: List[str] = []
                for cell in body_row.cells:
                    text_segment = cell.layout.text_anchor.text_segments[0]
                    row_data.append(
                        document.text[text_segment.start_index : text_segment.end_index]
                    )
                rows_data.append(row_data)

            # Reconstruct table content for simplicity or use the document.text directly
            table_content = "\n".join(["\t".join(row) for row in rows_data])

            bounding_box = []
            for vertex in table.layout.bounding_poly.normalized_vertices:
                bounding_box.extend([vertex.x, vertex.y])

            extracted_tables.append(
                ExtractedTable(
                    table_content=table_content,
                    rows=rows_data,
                    bounding_box=bounding_box,
                )
            )

    return extracted_tables
