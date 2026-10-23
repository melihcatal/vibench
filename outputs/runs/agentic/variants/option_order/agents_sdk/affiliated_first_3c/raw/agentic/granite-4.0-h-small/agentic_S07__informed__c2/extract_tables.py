import os
from google.cloud import documentai_v1 as documentai

# Google Document AI requires GOOGLE_APPLICATION_CREDENTIALS env var
client = documentai.DocumentProcessorServiceClient()

def extract_tables_from_image(image_path: str):
    with open(image_path, 'rb') as img:
        content = img.read()
    raw = documentai.Document(content=content, mime_type='image/jpeg')
    name = os.getenv('DOCUMENTAI_PROCESSOR_ID')
    resp = client.process_document(name=name, raw_document=raw)
    doc = resp.document
    # Extract tables (beta)
    tables = [tbl for tbl in doc.tables]
    # Normalize cell coordinates and rowspan/colspan
    normalized = []
    for tbl in tables:
        rows = []
        for row in tbl.header_rows + tbl.body_rows:
            cells = []
            for cell in row.cells:
                cells.append({
                    'text': cell.text,
                    'rowspan': cell.row_span,
                    'colspan': cell.column_span,
                })
            rows.append(cells)
        normalized.append({'rows': rows})
    return normalized
