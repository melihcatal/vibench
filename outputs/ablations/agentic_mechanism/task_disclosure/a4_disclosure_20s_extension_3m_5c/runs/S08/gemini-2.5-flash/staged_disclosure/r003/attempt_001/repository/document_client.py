
import os
from google.cloud import documentai_v1 as documentai

class DocumentExtractionClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client = documentai.DocumentProcessorServiceClient()

    def process_document(self, file_content: bytes, mime_type: str, processor_id: str):
        """
        Processes a document using Google Cloud Document AI.
        """
        processor_name = self.client.processor_path(self
.project_id, self.location, processor_id)
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document

    def get_processor_names(self):
        """
        Lists available processors for the given project and location.
        """
        parent = f"projects/{self.project_id}/locations/{self.location}"
        for processor in self.client.list_processors(parent=parent):
            print(f"Processor Name: {processor.display_name}, Type: {processor.type_}, ID: {processor.name.split('/')[-1]}")

if __name__ == '__main__':
    # Example usage (replace with your actual project ID, location, and processor ID)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "your-processor-id"  # e.g., "YOUR_PROCESSOR_ID"

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print("Please set GOOGLE_CLOUD_PROJECT environment variable and replace LOCATION and PROCESSOR_ID in the script.")
    else:
        client = DocumentExtractionClient(PROJECT_ID, LOCATION)
        # Example: List processors
        print("Listing available processors:")
        client.get_processor_names()

        # Example: Process a dummy document (replace with actual document processing logic)
        # with open("path/to/your/document.pdf", "rb") as f:
        #     document_content = f.read()
        #     mime_type = "application/pdf"
        #     processed_document = client.process_document(document_content, mime_type, PROCESSOR_ID)
        #     print("Document processed successfully.")
        #     # Further processing of the extracted entities can be done here
