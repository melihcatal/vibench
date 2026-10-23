from google.cloud import documentai_v1 as documentai
import os

class DocumentAIClient:
    def __init__(self):
        self.client = documentai.DocumentProcessorServiceClient()
        # PROJECT_ID, LOCATION, PROCESSOR_ID should be set as environment variables
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")

    def get_processor_path(self, processor_id: str) -> str:
        return self.client.processor_path(
            project=self.project_id,
            location=self.location,
            processor=processor_id,
        )

    def process_document(self, processor_id: str, document_content: bytes, mime_type: str):
        processor_path = self.get_processor_path(processor_id)
        raw_document = documentai.RawDocument(
            content=document_content,
            mime_type=mime_type
        )
        request = documentai.ProcessRequest(
            name=processor_path,
            raw_document=raw_document
        )
        response = self.client.process_document(request=request)
        return response.document
