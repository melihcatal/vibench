import os
from typing import Dict, Any, List
from document_client import DocumentAICLient
from document_models import DocumentExtractionRequest, TableExtractionResponse
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
GENERAL_PROCESSOR_ID = os.getenv(
    "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID", "your-general-processor-id"
)


def extract_tables_from_document(
    request: DocumentExtractionRequest,
) -> TableExtractionResponse:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    if not GENERAL_PROCESSOR_ID:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID environment variable not set."
        )

    document_ai_client = DocumentAICLient(location=request.location)
    document = document_ai_client.process_document(
        project_id=PROJECT_ID,
        processor_id=request.processor_id
        if request.processor_id != ""
        else GENERAL_PROCESSOR_ID,
        content=request.content,
        mime_type=request.mime_type,
    )

    tables_data = []
    for page in document.pages:
        for table in page.tables:
            current_table: Dict[str, Any] = {
                "page_number": page.page_number,
                "num_rows": table.header_rows[0]
                .layout.text_anchor.text_segments[0]
                .end_index
                if table.header_rows
                and table.header_rows[0].layout.text_anchor.text_segments
                else 0,  # Placeholder
                "num_columns": table.body_rows[0]
                .layout.text_anchor.text_segments[0]
                .end_index
                if table.body_rows
                and table.body_rows[0].layout.text_anchor.text_segments
                else 0,  # Placeholder
                "header_rows": [],
                "body_rows": [],
            }

            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append(
                        {
                            "text": documentai.Document.to_json(
                                cell.layout.text_anchor,
                                including_default_value_fields=False,
                            ),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                        }
                    )
                current_table["header_rows"].append(row_cells)

            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append(
                        {
                            "text": documentai.Document.to_json(
                                cell.layout.text_anchor,
                                including_default_value_fields=False,
                            ),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                        }
                    )
                current_table["body_rows"].append(row_cells)
            tables_data.append(current_table)

    return TableExtractionResponse(tables=tables_data)
