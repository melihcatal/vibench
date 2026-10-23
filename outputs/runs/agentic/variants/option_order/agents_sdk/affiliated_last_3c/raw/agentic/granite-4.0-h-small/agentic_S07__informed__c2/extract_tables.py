import os
from google.cloud import documentai_v1 as documentai
from document_models import DocumentTableResponse

class ExtractTables:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.processor_uri = "projects/PROJECT_ID/locations/us-central1/processors/processor_ID"
        self.client = documentai.DocumentProcessorServiceClient()

    def extract(self, image_path: str) -> DocumentTableResponse:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        name = self.processor_uri
        raw = documentai.RawDocument(content=image_bytes, mime_type="image/jpeg")
        doc = documentai.Document(raw_document=raw)
        request = documentai.ProcessRequest(name=name, document=doc)
        response = self.client.process_document(request=request)
        return DocumentTableResponse.from_api(response)

if __name__ == "__main__":
    tables = ExtractTables().extract("sample.jpg")
    for table in tables.tables:
        print(table.header_row)
