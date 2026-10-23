from google.cloud import documentai

from document_client import build_document_ai_client, build_raw_document


def extract_tables(payload, config=None):
    config = config or {}
    client = build_document_ai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": build_raw_document(payload)})
    tables = []
    for page in getattr(response.document, "pages", []) or []:
        for table in getattr(page, "tables", []) or []:
            tables.append({"header_rows": len(getattr(table, "header_rows", []) or []), "body_rows": len(getattr(table, "body_rows", []) or [])})
    return {"tables": tables}
