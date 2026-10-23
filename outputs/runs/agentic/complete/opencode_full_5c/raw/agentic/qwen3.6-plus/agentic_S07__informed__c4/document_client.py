import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "")
GOOGLE_LOCATION = os.environ.get("GOOGLE_LOCATION", "us")
GOOGLE_PROCESSOR_ID = os.environ.get("GOOGLE_PROCESSOR_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")


def get_document_ai_client():
    client_options = ClientOptions(
        api_endpoint=f"{GOOGLE_LOCATION}-documentai.googleapis.com"
    )
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def build_process_request(processor_name, file_bytes, mime_type="image/png"):
    return documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=file_bytes, mime_type=mime_type),
    )


def get_full_processor_name():
    return f"projects/{GOOGLE_PROJECT_ID}/locations/{GOOGLE_LOCATION}/processors/{GOOGLE_PROCESSOR_ID}"


def process_document(file_bytes, mime_type="image/png", processor_name=None):
    client = get_document_ai_client()
    name = processor_name or get_full_processor_name()
    request = build_process_request(name, file_bytes, mime_type)
    result = client.process_document(request=request)
    return result.document
