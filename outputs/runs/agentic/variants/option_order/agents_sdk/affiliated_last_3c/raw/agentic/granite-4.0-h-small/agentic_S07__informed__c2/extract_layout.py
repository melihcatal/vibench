import os
from google.cloud import documentai_v1 as documentai
from document_models import DocumentLayoutResponse

class ExtractLayout:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.processor_uri = "projects/PROJECT_ID/locations/us-central1/processors/processor_ID"
        self.client = documentai.DocumentProcessorServiceClient()

    def extract(self, image_path: str) -> DocumentLayoutResponse:
        with open(image_path, "rb") as f:
            image_data = f.read()
        name = self.processor_uri
        raw = documentai.RawDocument(content=image_data, mime_type="image/jpeg")
        doc = documentai.Document(raw_document=raw)
        request = documentai.ProcessRequest(name=name, document=doc)
        response = self.client.process_document(request=request)
        return DocumentLayoutResponse.from_api(response)

if __name__ == "__main__":
    layout = ExtractLayout().extract("sample.jpg")
    print(layout.blocks)
