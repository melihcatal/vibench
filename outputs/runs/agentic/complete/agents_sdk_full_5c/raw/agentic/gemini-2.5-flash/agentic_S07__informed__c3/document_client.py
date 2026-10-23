import os
from google.cloud import documentai_v1beta3 as documentai

class DocumentAICLient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        self.client = documentai.DocumentProcessorServiceClient(client_options=self.client_options)

    def get_processor_name(self, processor_id: str) -> str:
        return self.client.processor_path(self.project_id, self.location, processor_id)

    def process_document(self, processor_id: str, file_content: bytes, mime_type: str):
        name = self.get_processor_name(processor_id)
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        return self.client.process_document(request=request)

    @staticmethod
    def load_document_content(file_path: str) -> bytes:
        with open(file_path, "rb") as image:
            return image.read()

if __name__ == '__main__':
    # Example usage (not part of the core functionality, but for testing/demonstration)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR")
    # client = DocumentAICLient(project_id, location)
    # file_content = client.load_document_content("path/to/your/document.pdf")
    # result = client.process_document(processor_id, file_content, "application/pdf")
    # print("Document processed successfully.")
