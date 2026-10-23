import os
from google.cloud import documentai

class ExtractText:
    def __init__(self, project_id: str = None, location: str = 'us', processor_id: str = 'document/text_extraction'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or 'your-gcp-project'
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceClient()

    def process(self, image_bytes: bytes) -> str:
        # Build the document
        document = {'content': image_bytes, 'mime_type': 'image/png'}
        # Create the request
        request = {'name': f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}", 'document': document}
        # Call the API
        response = self.client.process_document(request=request)
        # Extract text
        document_text = response.document.text
        return document_text
