from google.cloud import documentai_v1 as documentai
import os

class DocumentClient:
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = self.client.processor_path(project_id, location, processor_id)

    def process_document(self, document_content: bytes, mime_type: str) -> documentai.Document:
        """
        Processes a document using the configured Document AI processor.
        """
        raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=self.processor_name, raw_document=raw_document)
        result = self.client.process_document(request=request)
        return result.document

# Example configuration (can be loaded from environment variables or a config file)
# PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
# LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us" or "eu"
# PROCESSOR_ID = os.getenv("GOOGLE_CLOUD_PROCESSOR_ID") # e.g., your-processor-id

# if __name__ == "__main__":
#     # This is an example of how to use the DocumentClient
#     # You would need to replace these with your actual project, location, and processor IDs
#     # and provide actual document content and mime type.
#     sample_project_id = "your-gcp-project-id"
#     sample_location = "us"
#     sample_processor_id = "your-document-ai-processor-id"

#     if not all([sample_project_id, sample_location, sample_processor_id]):
#         print("Please set your Google Cloud project ID, location, and processor ID.")
#     else:
#         client = DocumentClient(sample_project_id, sample_location, sample_processor_id)
#         # In a real scenario, document_content would be read from a file or another source
#         # For example:
#         # with open("path/to/your/document.pdf", "rb") as image_file:
#         #     document_content = image_file.read()
#         # mime_type = "application/pdf"
#         # document = client.process_document(document_content, mime_type)
#         # print("Document processed successfully!")
#         # print(f"Text: {document.text[:500]}...") # Print first 500 characters of extracted text
