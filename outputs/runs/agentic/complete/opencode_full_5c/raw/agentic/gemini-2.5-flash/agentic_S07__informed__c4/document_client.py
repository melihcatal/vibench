import os
from google.cloud import documentai_v1 as documentai


class DocumentAIClient:
    """
    A client for interacting with Google Cloud Document AI.
    """

    def __init__(self, project_id: str = None, location: str = "us"):
        self.project_id = (
            project_id if project_id else os.environ.get("GOOGLE_CLOUD_PROJECT")
        )
        if not self.project_id:
            raise ValueError(
                "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set."
            )
        self.location = location
        self.client = documentai.DocumentProcessorServiceClient()

    def get_processor_name(self, processor_id: str) -> str:
        """
        Constructs the full resource name for a Document AI processor.
        """
        return self.client.processor_path(self.project_id, self.location, processor_id)

    def process_document(
        self, file_content: bytes, mime_type: str, processor_id: str
    ) -> documentai.Document:
        """
        Processes a document using the specified Document AI processor.
        """
        processor_name = self.get_processor_name(processor_id)

        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        result = self.client.process_document(request=request)
        return result.document
