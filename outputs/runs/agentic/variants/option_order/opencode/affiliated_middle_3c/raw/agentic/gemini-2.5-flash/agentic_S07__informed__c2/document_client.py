import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


class DocumentAICLient:
    def __init__(self, location: str = "us"):
        self.location = location
        self.client = self._get_documentai_client()

    def _get_documentai_client(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
        # For more details, see: https://cloud.google.com/docs/authentication/production
        client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        return documentai.DocumentProcessorServiceClient(client_options=client_options)

    def process_document(
        self, project_id: str, processor_id: str, content: bytes, mime_type: str
    ) -> documentai.Document:
        processor_name = self.client.processor_path(
            project_id, self.location, processor_id
        )
        raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
        request = documentai.ProcessRequest(
            name=processor_name, raw_document=raw_document
        )
        result = self.client.process_document(request=request)
        return result.document
