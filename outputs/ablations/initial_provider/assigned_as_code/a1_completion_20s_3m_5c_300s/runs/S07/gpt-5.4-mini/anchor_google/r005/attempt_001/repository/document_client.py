from google.cloud import documentai


DEFAULT_LOCATION = "us"


def normalize_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", DEFAULT_LOCATION),
        "processor_id": config.get("processor_id"),
        "token": config.get("token"),
        "model_id": config.get("model_id"),
        "ocr_model": config.get("ocr_model"),
    }


def make_documentai_client(location):
    return documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})
