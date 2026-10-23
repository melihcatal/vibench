import os
from google.cloud import documentai


class DocumentAIClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")

        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

        self.client = documentai.DocumentProcessorServiceClient()

    def get_processor_path(self, processor_name: str) -> str:
        return self.client.processor_path(
            self.project_id, self.location, processor_name
        )

    def process_document(
        self, processor_name: str, file_content: bytes, mime_type: str
    ):
        processor_path = self.get_processor_path(processor_name)

        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

        request = documentai.ProcessRequest(
            name=processor_path, raw_document=raw_document
        )

        result = self.client.process_document(request=request)
        return result.document
