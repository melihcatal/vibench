from google.cloud import documentai

from document_client import build_processor_name, get_config, get_document_ai_client


def extract_tables(image_bytes: bytes, mime_type: str = "image/png"):
    cfg = get_config()
    client = get_document_ai_client()
    name = build_processor_name(cfg["project_id"], cfg["location"], cfg["processor_id"])
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    tables = []
    for page in response.document.pages:
        for table in page.tables:
            rows = []
            for row in table.header_rows + table.body_rows:
                rows.append([cell.layout.text_anchor for cell in row.cells])
            tables.append({"rows": rows})
    return tables
