import os
from google.cloud import documentai

class ExtractTables:
    def __init__(self, project_id: str = None, location: str = 'us', processor_id: str = 'document/table_extraction'):
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
        # Normalize tables
        tables = []
        for entity in response.document.entities:
            if entity.type_ == 'TABLE':
                rows = []
                for row in entity.page_anchor.start_token_index:
                    # Simplified: collect row cells
                    rows.append([cell.text for cell in entity.cells]) 
                tables.append({'rows': rows})
        return {'tables': tables, 'raw_response': response}
