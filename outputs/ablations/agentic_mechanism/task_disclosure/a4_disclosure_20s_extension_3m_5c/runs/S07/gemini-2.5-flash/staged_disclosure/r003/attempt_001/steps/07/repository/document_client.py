
import os
from google.cloud import documentai_v1 as documentai

class DocumentClient:
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = self.client.processor_path(
            project_id, location, processor_id
        )

    def process_document(self, file_content: bytes, mime_type: str):
        """
        Processes a document using the Document AI processor.
        Args:
            file_content: The content of the document file as bytes.
            mime_type: The MIME type of the document (e.g., "application/pdf").
        Returns:
            A Document object containing the processing results.
        """
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=self.processor_name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document

if __name__ == '__main__':
    # Example usage (replace with your actual project_id, location, and processor_id)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
    PROCESSOR_ID = os.environ.get("GOOGLE_CLOUD_PROCESSOR_ID", "your-processor-id") # e.g., "YOUR_PROCESSOR_ID" for OCR

    if PROJECT_ID == "your-gcp-project-id" or PROCESSOR_ID == "your-processor-id":
        print("Please set GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_PROCESSOR_ID environment variables or update the placeholder values.")
    else:
        document_client = DocumentClient(PROJECT_ID, LOCATION, PROCESSOR_ID)

        # Example: Read a dummy PDF file (replace with your actual file)
        # For a real scenario, you would read a PDF, TIFF, or JPEG file.
        # with open("path/to/your/document.pdf", "rb") as image:
        #     image_content = image.read()
        #     mime_type = "application/pdf"

        #     print(f"Processing document with processor: {document_client.processor_name}")
        #     document = document_client.process_document(image_content, mime_type)
        #     print("Document processing complete.")
        #     print(f"Text: {document.text}")
        #     # Further processing of entities, pages, etc.
