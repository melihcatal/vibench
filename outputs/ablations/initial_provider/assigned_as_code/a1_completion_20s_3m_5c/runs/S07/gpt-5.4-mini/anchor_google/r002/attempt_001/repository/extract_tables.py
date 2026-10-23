from google.cloud import documentai

from document_client import load_config, make_client, processor_name, raw_document
from document_models import normalize_tables


def extract_tables(payload, config=None):
    config = load_config(config)
    client = make_client(config)
    name = processor_name(client, config)
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    tables = []
    for page in response.document.pages:
        for table in page.tables:
            header_rows = []
            body_rows = []
            for row in table.header_rows:
                header_rows.append([cell.layout.text_anchor.content if cell.layout.text_anchor else "" for cell in row.cells])
            for row in table.body_rows:
                body_rows.append([cell.layout.text_anchor.content if cell.layout.text_anchor else "" for cell in row.cells])
            tables.append({"header_rows": header_rows, "body_rows": body_rows})
    return {"tables": normalize_tables(tables)}
