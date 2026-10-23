from google.cloud import documentai


def document_field_extraction(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])})
    fields = {}
    for page in response.document.pages:
        for field in page.form_fields:
            key = field.field_name.text_anchor.content if field.field_name.text_anchor else ""
            value = field.field_value.text_anchor.content if field.field_value.text_anchor else ""
            fields[key] = value
    return {"fields": fields}
