import os
from dataclasses import dataclass


@dataclass
class DocumentClientConfig:
    endpoint: str
    api_key: str
    model_id: str = "prebuilt-layout"


def load_document_client_config(config=None):
    config = config or {}
    return DocumentClientConfig(
        endpoint=config.get("endpoint") or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        api_key=config.get("api_key") or os.environ["AZURE_DOCUMENT_INTELLIGENCE_API_KEY"],
        model_id=config.get("model_id") or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout"),
    )


def document_intelligence_headers(api_key):
    return {"Ocp-Apim-Subscription-Key": api_key}
