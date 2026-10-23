import os
from google.cloud import documentai

class ExtractLayout:
    def __init__(self, project_id: str = None, location: str = 'us', processor_id: str = 'document/layout'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or 'your-gcp-project'
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceClient()

    def process(self, image_bytes: bytes) -> dict:
        # Prepare the document
        document = {'content': image_bytes, 'mime_type': 'image/png'}
        # Build the request
        request = {'name': f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}", 'document': document}
        # Call the API
        response = self.client.process_document(request=request)
        # Return normalized layout elements
        layout_elements = []
        for ent in response.document.entities:
            layout_elements.append({
                'type': ent.type_,
                'text': ent.text,
                'bounding_poly': ent.layout.bounding_poly.vertices
            })
        return {'layout_elements': layout_elements, 'raw_response': response}
