import os
from google.cloud import documentai


def extract_structured_fields(text):
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "YOUR_PROCESSOR_ID"
    processor = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    document = documentai.Document(content=text, mime_type="text/plain")
    response = client.process_document(name=processor, document=document)
    return response.document
