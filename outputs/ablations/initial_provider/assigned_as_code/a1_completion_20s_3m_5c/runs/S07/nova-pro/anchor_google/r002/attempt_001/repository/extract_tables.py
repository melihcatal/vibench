from google.cloud import documentai


def extract_tables(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    tables = []
    for page in response.document.pages:
        for table in page.tables:
            table_data = {
                "header_rows": [],
                "body_rows": [],
                "footer_rows": []
            }
            for row in table.header_rows:
                table_data["header_rows"].append([cell.text for cell in row.cells])
            for row in table.body_rows:
                table_data["body_rows"].append([cell.text for cell in row.cells])
            for row in table.footer_rows:
                table_data["footer_rows"].append([cell.text for cell in row.cells])
            tables.append(table_data)
    return {"tables": tables}