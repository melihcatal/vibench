import os
from typing import List, Optional

from google.cloud import documentai_v1 as documentai

from document_client import get_gcp_documentai_processor_path
from document_models import DocumentInput, TableExtractionOutput, Table, TableRow, TableCell

def extract_document_tables(
    document_input: DocumentInput,
    processor_id: Optional[str] = None,
) -> TableExtractionOutput:
    """Extracts tables from a document using Google Cloud Document AI's Form Parser or Table Processor."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us")
    # Use a processor suitable for table extraction, e.g., Form Parser or a custom processor.
    default_processor_id = os.environ.get("GCP_DOCUMENTAI_TABLE_PROCESSOR_ID", "FORM_PARSER_PROCESSOR_ID_HERE")

    processor_name = get_gcp_documentai_processor_path(
        project_id, location, processor_id or default_processor_id
    )

    client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(
        content=document_input.image_bytes,
        mime_type=document_input.mime_type,
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_tables: List[Table] = []

    for page in document.pages:
        for doc_table in page.tables:
            rows: List[TableRow] = []
            # Headers (optional)
            if doc_table.header_rows:
                header_cells: List[TableCell] = []
                for cell in doc_table.header_rows[0].cells:
                    text = documentai.get_text_anchor_text(cell.layout.text_anchor, document.text)
                    header_cells.append(TableCell(text=text, row_span=cell.row_span, col_span=cell.col_span))
                rows.append(TableRow(cells=header_cells))

            # Body rows
            for doc_row in doc_table.body_rows:
                body_cells: List[TableCell] = []
                for cell in doc_row.cells:
                    text = documentai.get_text_anchor_text(cell.layout.text_anchor, document.text)
                    body_cells.append(TableCell(text=text, row_span=cell.row_span, col_span=cell.col_span))
                rows.append(TableRow(cells=body_cells))
            extracted_tables.append(Table(rows=rows))

    return TableExtractionOutput(tables=extracted_tables)
