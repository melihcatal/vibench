import os
from google.cloud import documentai

class ExtractKeyValues:
    def __init__(self, project_id: str = None, location: str = 'us', processor_id: str = 'document/key_value_extraction'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or 'your-gcp-project'
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceClient()

    def process(self, image_bytes: bytes):
        # Build the document
        document = {'content': image_bytes, 'mime_type': 'image/png'}
        # Create request
        request = {'name': f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}", 'document': document}
        # Call API
        response = self.client.process_document(request=request)
        # Extract key-value pairs
        kv_pairs = {}
        for entity in response.document.entities:
            if entity.type_ == 'KEY_VALUE_SET':
                key = next((e.text for e in entity.entities if e.type_ == 'KEY'), None)
                value = next((e.text for e in entity.entities if e.type_ == 'VALUE'), None)
                if key and value:
                    kv_pairs[key] = value
        return {'key_value_pairs': kv_pairs, 'raw_response': response}
