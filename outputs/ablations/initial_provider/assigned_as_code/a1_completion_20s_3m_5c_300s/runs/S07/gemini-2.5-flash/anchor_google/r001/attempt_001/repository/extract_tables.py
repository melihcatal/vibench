from google.cloud import documentai
from document_client import get_document_ai_client
from document_models import DocumentAIConfig, DocumentPayload

def extract_tables(payload: DocumentPayload, config: DocumentAIConfig):
    client = get_document_ai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)
    
    raw_document = documentai.RawDocument(content=payload.document_bytes, mime_type=payload.mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    
    response = client.process_document(request=request)
    
    extracted_tables = []
    for page in response.document.pages:
        for table in page.tables:
            table_data = {"body_rows": [], "header_rows": []}
            for row in table.body_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(cell.layout.text_anchor.text_segments[0].start_index)
                table_data["body_rows"].append(row_cells)
            for row in table.header_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append(cell.layout.text_anchor.text_segments[0].start_index)
                table_data["header_rows"].append(row_cells)
            extracted_tables.append(table_data)

    return {"tables": extracted_tables}
