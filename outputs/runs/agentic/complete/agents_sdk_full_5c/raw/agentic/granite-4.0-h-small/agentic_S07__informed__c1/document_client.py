import os
from google.cloud import documentai

class DocumentClient:
    def __init__(self, project_id: str = None, location: str = 'us'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or 'your-gcp-project'
        self.location = location
        self.processor_id = 'document/text_extraction'  # default processor for OCR
        self.client = documentai.DocumentProcessorServiceClient()

    def _build_request(self, image_bytes: bytes, processor_id: str = None):
        processor_id = processor_id or self.processor_id
        document = {'content': image_bytes, 'mime_type': 'image/png'}
        return {
            'name': f"projects/{self.project_id}/locations/{self.location}/processors/{processor_id}",
            'document': document
        }

    def extract_text(self, image_bytes: bytes):
        request = self._build_request(image_bytes)
        response = self.client.process_document(request=request)
        return response.document.text

    def extract_layout(self, image_bytes: bytes):
        request = self._build_request(image_bytes, processor_id='document/layout')
        response = self.client.process_document(request=request)
        layout = []
        for ent in response.document.entities:
            layout.append({
                'type': ent.type_,
                'text': ent.text,
                'poly': [pt for pt in ent.layout.bounding_poly.vertices]
            })
        return layout

    def extract_tables(self, image_bytes: bytes):
        request = self._build_request(image_bytes, processor_id='document/table_extraction')
        response = self.client.process_document(request=request)
        tables = []
        for entity in response.document.entities:
            if entity.type_ == 'TABLE':
                rows = []
                for cell in entity.cells:
                    rows.append(cell.text)
                tables.append({'rows': rows})
        return tables

    def extract_key_values(self, image_bytes: bytes):
        request = self._build_request(image_bytes, processor_id='document/key_value_extraction')
        response = self.client.process_document(request=request)
        kv = {}
        for entity in response.document.entities:
            if entity.type_ == 'KEY_VALUE_SET':
                key = next((e.text for e in entity.entities if e.type_ == 'KEY'), None)
                value = next((e.text for e in entity.entities if e.type_ == 'VALUE'), None)
                if key and value:
                    kv[key] = value
        return kv
