from document_client import get_documentai_client, get_project_id, get_location
from document_models import (
    DocumentTableExtractionResponse,
    DocumentTable,
    DocumentTableCell,
)
from google.cloud import documentai_v1beta3 as documentai
import os


def extract_tables_from_document(
    document_content: bytes, mime_type: str
) -> DocumentTableExtractionResponse:
    project_id = get_project_id()
    location = get_location()
    # Replace with your actual processor ID for table extraction
    processor_id = os.getenv(
        "DOCUMENT_AI_TABLE_PROCESSOR_ID", "YOUR_TABLE_PROCESSOR_ID"
    )

    if processor_id == "YOUR_TABLE_PROCESSOR_ID":
        raise ValueError(
            "DOCUMENT_AI_TABLE_PROCESSOR_ID environment variable not set or is default. Please configure your Document AI table processor ID."
        )

    client = get_documentai_client()

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []
    for page in document.pages:
        for table in page.tables:
            cells = []
            for row_index, row in enumerate(table.body_rows):
                for col_index, cell in enumerate(row.cells):
                    cell_text = "".join(
                        [
                            text_segment.text_content
                            for text_segment in cell.layout.text_anchor.text_segments
                        ]
                    )
                    cells.append(
                        DocumentTableCell(
                            row_index=row_index, col_index=col_index, text=cell_text
                        )
                    )
            extracted_tables.append(
                DocumentTable(
                    cells=cells,
                    num_rows=len(table.body_rows),
                    num_columns=len(table.header_rows[0].cells)
                    if table.header_rows
                    else 0,  # Assuming consistent columns
                )
            )

    return DocumentTableExtractionResponse(tables=extracted_tables)
