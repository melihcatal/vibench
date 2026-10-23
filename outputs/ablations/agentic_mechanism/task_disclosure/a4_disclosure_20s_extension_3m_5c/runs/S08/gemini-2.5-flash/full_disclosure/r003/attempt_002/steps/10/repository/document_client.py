import os
from google.cloud import documentai_v1 as documentai

class DocumentExtractionConfig:
    """
    Local configuration for Structured Document Extraction.
    """
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id

class DocumentAIClient:
    """
    Client helper utilities for Structured Document Extraction using Google Cloud Document AI.
    """
    def __init__(self, config: DocumentExtractionConfig):
        self.config = config
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = self.client.processor_path(
            self.config.project_id, self.config.location, self.config.processor_id
        )

    def extract_document(self, document_content: bytes, mime_type: str):
        """
        Extracts structured data from a document using Google Cloud Document AI.

        Args:
            document_content: The content of the document (e.g., PDF, JPEG).
            mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

        Returns:
            A Document object containing the extracted entities.
        """
        raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=self.processor_name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document
