from google.cloud import documentai


def get_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", "us"),
        "processor_id": config.get("processor_id"),
        "form_processor_id": config.get("form_processor_id", config.get("processor_id")),
        "layout_processor_id": config.get("layout_processor_id", config.get("processor_id")),
        "table_processor_id": config.get("table_processor_id", config.get("processor_id")),
        "text_processor_id": config.get("text_processor_id", config.get("processor_id")),
        "translation_target_language": config.get("translation_target_language", "en"),
    }


def get_client(location):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )


def processor_path(client, project_id, location, processor_id):
    return client.processor_path(project_id, location, processor_id)


def raw_document(payload):
    return documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])
