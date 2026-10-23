import os
from google.cloud import documentai


def load_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ["DOCUMENTAI_PROJECT_ID"],
        "location": config.get("location") or os.environ.get("DOCUMENTAI_LOCATION", "us"),
        "processor_id": config.get("processor_id") or os.environ["DOCUMENTAI_PROCESSOR_ID"],
        "form_processor_id": config.get("form_processor_id") or os.environ.get("DOCUMENTAI_FORM_PROCESSOR_ID"),
        "layout_processor_id": config.get("layout_processor_id") or os.environ.get("DOCUMENTAI_LAYOUT_PROCESSOR_ID"),
        "table_processor_id": config.get("table_processor_id") or os.environ.get("DOCUMENTAI_TABLE_PROCESSOR_ID"),
    }


def build_client(config=None):
    config = load_config(config)
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    ), config


def processor_name(client, config, processor_id=None):
    return client.processor_path(
        config["project_id"],
        config["location"],
        processor_id or config["processor_id"],
    )
