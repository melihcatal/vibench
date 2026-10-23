import os
from google.cloud import documentai


def extract_fields(document_path):
    client = documentai.DocumentProcessorServiceClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    with open(document_path, "rb") as document_file:
        document = documentai.Document(
            content=document_file.read(), mime_type="application/pdf"
        )
        request = documentai.ProcessDocumentRequest(
            name="projects/project-id/locations/location-id/processors/processor-id",
            document=document,
        )
        result = client.process_document(request=request)
        return result.entities
