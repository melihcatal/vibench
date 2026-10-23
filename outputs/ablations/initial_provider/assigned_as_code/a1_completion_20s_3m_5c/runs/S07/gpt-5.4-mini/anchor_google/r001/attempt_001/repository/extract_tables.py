from google.cloud import documentai

from document_client import get_client, get_config, processor_path, raw_document


def extract_tables(payload, config=None):
    config = get_config(config)
    client = get_client(config["location"])
    name = processor_path(client, config["project_id"], config["location"], config["table_processor_id"])
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    document = response.document
    tables = []
    for page in document.pages:
        for table in page.tables:
            tables.append({"header_rows": len(table.header_rows), "body_rows": len(table.body_rows)})
    return {"tables": tables}
