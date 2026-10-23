import os
from google.cloud import documentai


class DocumentAIClient:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.location = os.getenv("GCP_LOCATION", "us")
        self.processor_id = os.getenv("GCP_PROCESSOR_ID")

        if not all([self.project_id, self.location, self.processor_id]):
            raise ValueError(
                "Missing GCP configuration for Document AI in environment variables."
            )

        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = self.client.processor_path(
            self.project_id, self.location, self.processor_id
        )

    def process_document(self, file_path: str, mime_type: str = "application/pdf"):
        with open(file_path, "rb") as image:
            image_content = image.read()

        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )

        request = documentai.ProcessRequest(
            name=self.processor_name, raw_document=raw_document
        )

        result = self.client.process_document(request=request)
        return result.document
