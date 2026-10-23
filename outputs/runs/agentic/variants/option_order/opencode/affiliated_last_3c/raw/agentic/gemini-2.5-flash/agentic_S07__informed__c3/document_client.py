from google.cloud import documentai_v1 as documentai
import os


class DocumentAICLient:
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.opts = {"api_endpoint": f"{self.location}-documentai.googleapis.com"}
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=self.opts
        )
        self.processor_name = self.client.processor_path(
            project_id, location, processor_id
        )

    def process_document(self, file_content: bytes, mime_type: str):
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(
            name=self.processor_name, raw_document=raw_document
        )
        result = self.client.process_document(request=request)
        return result.document


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    # client = DocumentAICLient(project_id, location, processor_id)
    # with open("path/to/your/document.pdf", "rb") as f:
    #     content = f.read()
    # document = client.process_document(content, "application/pdf")
    # print(document.text)
