from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentInput, DocumentOutput
import os


def extract_tables_from_document(document_input: DocumentInput) -> DocumentOutput:
    client = get_document_ai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get(
        "DOCUMENT_AI_TABLE_PROCESSOR_ID"
    )  # Specific table processor or general

    if not processor_id:
        raise ValueError(
            "DOCUMENT_AI_TABLE_PROCESSOR_ID environment variable not set. Consider using a general document processor or a specific table processor."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document

    all_tables = []
    for page in document.pages:
        for table in page.tables:
            header_rows = []
            for row in table.header_rows:
                cells = []
                for cell in row.cells:
                    cells.append(cell.text_anchor.content)
                header_rows.append(cells)

            body_rows = []
            for row in table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append(cell.text_anchor.content)
                body_rows.append(cells)

            all_tables.append(
                {
                    "page_number": page.page_number,
                    "header_rows": header_rows,
                    "body_rows": body_rows,
                }
            )

    return DocumentOutput(tables=all_tables, text=document.text)
