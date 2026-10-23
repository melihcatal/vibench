from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


class DocumentAIManager:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        self.client = documentai.DocumentProcessorServiceClient(client_options=self.client_options)

    def process_document(self, processor_id: str, document_bytes: bytes, mime_type: str):
        processor_name = self.client.processor_path(self.project_id, self.location, processor_id)
        raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
        request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document
