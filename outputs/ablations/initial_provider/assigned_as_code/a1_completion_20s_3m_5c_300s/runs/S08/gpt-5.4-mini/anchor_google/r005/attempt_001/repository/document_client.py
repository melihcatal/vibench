from google.cloud import documentai


def load_documentai_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", "us"),
        "processor_id": config.get("processor_id"),
        "api_endpoint": f"{config.get('location', 'us')}-documentai.googleapis.com",
    }


def build_documentai_client(config=None):
    cfg = load_documentai_config(config)
    return documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": cfg["api_endpoint"]})
