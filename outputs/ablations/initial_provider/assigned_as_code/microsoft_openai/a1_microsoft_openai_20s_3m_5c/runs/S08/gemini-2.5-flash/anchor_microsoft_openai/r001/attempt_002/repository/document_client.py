import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

class DocumentClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        )

    def process_document(self, processor_name: str, document_bytes: bytes, mime_type: str):
        name = self.client.processor_path(self.project_id, self.location, processor_name)
        raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document
