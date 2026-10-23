import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentTable, TableCell

def extract_tables(image_content: bytes, mime_type: str = "application/pdf") -> list[DocumentTable]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_TABLES")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, or GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_TABLES environment variables.")

    processor_name = client.processor_path(project_id, location, processor_id)
    client = get_document_ai_client()

    document = documentai.Document(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, document=document)

    response = client.process_document(request=request)

    extracted_tables = []
    if response.document and response.document.pages:
        for page in response.document.pages:
            for table in page.tables:
                header_rows = []
                body_rows = []

                for row in table.header_rows:
                    cells = []
                    for cell in row.cells:
                        text = response.document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index] if cell.layout.text_anchor.text_segments else ""
                        cells.append(TableCell(text=text, row_span=cell.row_span, col_span=cell.col_span))
                    header_rows.append(cells)
                
                for row in table.body_rows:
                    cells = []
                    for cell in row.cells:
                        text = response.document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index] if cell.layout.text_anchor.text_segments else ""
                        cells.append(TableCell(text=text, row_span=cell.row_span, col_span=cell.col_span))
                    body_rows.append(cells)
                
                extracted_tables.append(DocumentTable(header_rows=header_rows, body_rows=body_rows))

    return extracted_tables
