import os
from google.cloud import documentai_v1 as documentai
import document_client

def extract_tables(image_path: str) -> list[dict]:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us'
    processor_id = os.getenv('GOOGLE_DOCUMENT_AI_PROCESSOR_ID')
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client = documentai.DocumentProcessorServiceClient()
    image_bytes = document_client.load_image(image_path)
    mime_type = document_client.get_mimetype(image_path)
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    tables = []
    if document.pages:
        page = document.pages[0]
        for table_idx, table in enumerate(page.tables or []):
            table_data = []
            for row in table.table_rows:
                row_data = []
                for cell in row.table_cells:
                    cell_text = ''
                    for paragraph in cell.paragraphs:
                        start = paragraph.start_index
                        end = paragraph.end_index
                        cell_text += document.text[start:end]
                    row_data.append(cell_text)
                table_data.append(row_data)
            tables.append({'table_id': table_idx, 'structure': table_data})
    return tables
