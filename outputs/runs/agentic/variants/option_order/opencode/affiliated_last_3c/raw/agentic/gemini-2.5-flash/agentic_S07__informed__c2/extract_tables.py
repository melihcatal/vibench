import os
from typing import Dict, Any, List
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentInput, DocumentOutput


def extract_tables_from_document(
    document_input: DocumentInput, project_id: str, location: str, processor_id: str
) -> DocumentOutput:
    """Extracts table cells and row structure from a document using Google Document AI.
    Requires a processor trained for table extraction.
    """
    client = get_documentai_client()
    processor_name = get_processor_name(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    response = client.process_document(request=request)
    document = response.document

    tables_data: List[Dict[str, Any]] = []
    for page in document.pages:
        for table_index, table in enumerate(page.tables):
            current_table: Dict[str, Any] = {
                "page_number": page.page_number,
                "table_index": table_index,
                "header_rows": [],
                "body_rows": [],
            }
            # Extract header rows
            for row in table.header_rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(
                        document.text[
                            cell.layout.text_anchor.text_segments[
                                0
                            ].start_index : cell.layout.text_anchor.text_segments[
                                0
                            ].end_index
                        ]
                        if cell.layout.text_anchor.text_segments
                        else ""
                    )
                current_table["header_rows"].append(row_data)

            # Extract body rows
            for row in table.body_rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(
                        document.text[
                            cell.layout.text_anchor.text_segments[
                                0
                            ].start_index : cell.layout.text_anchor.text_segments[
                                0
                            ].end_index
                        ]
                        if cell.layout.text_anchor.text_segments
                        else ""
                    )
                current_table["body_rows"].append(row_data)
            tables_data.append(current_table)

    return DocumentOutput(text=document.text, tables=tables_data)
