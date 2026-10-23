import os
from typing import Any, Dict

from openai import OpenAI

from document_models import DocumentRequest, encode_source_to_data_uri


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_azure_document_intelligence_endpoint() -> str:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    return endpoint.rstrip("/")


def get_azure_document_intelligence_key() -> str:
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return key


def prepare_image_input(request: DocumentRequest) -> Dict[str, Any]:
    return {"image": encode_source_to_data_uri(request.source), "language": request.language, "metadata": request.metadata}
