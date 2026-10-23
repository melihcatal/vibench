import os
from google.cloud import documentai_v1 as documentai
from document_models import DocumentResponse

class ExtractText:
    def __init__(self):
        # Uses Google Cloud credentials from environment variable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.processor_uri = "projects/PROJECT_ID/locations/us-central1/processors/processor_ID"
        self.client = documentai.DocumentProcessorServiceClient()

    def extract(self, image_path: str) -> DocumentResponse:
        # Read the image file
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        # Prepare the request
        name = self.processor_uri
        raw_document = documentai.RawDocument(content=content, mime_type="image/jpeg")
        document = documentai.Document(raw_document=raw_document)
        request = documentai.ProcessRequest(name=name, document=document)
        # Call the Document AI OCR processor
        response = self.client.process_document(request=request)
        # Convert to normalized response
        return DocumentResponse.from_api(response)

if __name__ == "__main__":
    extractor = ExtractText()
    result = extractor.extract("sample.jpg")
    print(result.text)
