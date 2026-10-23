from google.cloud import documentai

from document_client import normalize_config, make_documentai_client


def extract_tables(payload, config=None):
    config = normalize_config(config)
    client = make_documentai_client(config["location"])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])})
    tables = []
    for page in response.document.pages:
        for table in page.tables:
            rows = []
            for row in table.header_rows + table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append({"text": cell.layout.text_anchor.content if hasattr(cell.layout.text_anchor, "content") else ""})
                rows.append({"cells": cells})
            tables.append({"rows": rows})
    return {"tables": tables}
