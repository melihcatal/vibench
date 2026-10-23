import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    opts = ClientOptions(
        api_endpoint=os.getenv(
            "GOOGLE_DOCUMENT_AI_ENDPOINT", "us-documentai.googleapis.com"
        )
    )
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client
