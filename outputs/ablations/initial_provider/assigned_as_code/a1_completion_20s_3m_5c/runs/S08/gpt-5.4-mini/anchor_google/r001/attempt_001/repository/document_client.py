from functools import lru_cache
import os

from google.cloud import documentai


def load_documentai_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("DOCUMENTAI_PROJECT_ID"),
        "location": config.get("location") or os.environ.get("DOCUMENTAI_LOCATION", "us"),
        "processor_id": config.get("processor_id") or os.environ.get("DOCUMENTAI_PROCESSOR_ID"),
    }


@lru_cache(maxsize=1)
def get_documentai_client(location="us"):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )


def build_processor_name(project_id, location, processor_id):
    client = get_documentai_client(location)
    return client.processor_path(project_id, location, processor_id)
