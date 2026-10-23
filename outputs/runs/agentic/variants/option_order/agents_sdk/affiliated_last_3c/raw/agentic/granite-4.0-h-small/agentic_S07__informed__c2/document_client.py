import os
from google.cloud import documentai_v1 as documentai

class DocumentClient:
    def __init__(self):
        # Uses credentials from environment
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.processor_uri = "projects/PROJECT_ID/locations/us-central1/processors/processor_ID"
        self.client = documentai.DocumentProcessorServiceClient()

    def process(self, image_path: str, processor_uri: str | None = None) -> str:
        proc_uri = processor_uri or self.processor_uri
        with open(image_path, "rb") as f:
            image_data = f.read()
        raw_doc = documentai.RawDocument(content=image_data, mime_type="image/jpeg")
        doc = documentai.Document(raw_document=raw_doc)
        request = documentai.ProcessRequest(name=proc_uri, document=doc)
        response = self.client.process_document(request=request)
        # Return the raw response JSON for downstream processing
        return response.to_json()
