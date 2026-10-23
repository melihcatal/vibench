import os
import json
from typing import List, Dict
from google.cloud import documentai_v1beta3 as ga_docai

# Service identifier:
# Provider: Google Document AI (structured field extraction)

API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PROJECT_ID = 'your-project-id'
LOCATION = 'us-central1'
PROCESSOR_ID = 'projects/{}/locations/{}/processors/{}'.format(PROJECT_ID, LOCATION, os.getenv('STRUCTURED_PROCESSOR_ID'))

class DocumentFieldExtractor:
    def __init__(self):
        self._client = ga_docai.DocumentProcessorServiceClient()

    def extract_fields(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """Extract structured fields from OCR-normalized document text.

        Args:
            image_bytes: binary document image.

        Returns:
            List of dictionaries representing detected key‑value pairs and table rows.
        """
        # Create a Document proto
        document = ga_docai.Document.fromJson({"content": image_bytes, "mime_type": "image/jpeg"})
        # Request processing (use the processor specialized for form parsing, e.g., invoice)
        response = self._client.process_document(name=PROCESSOR_ID, raw_document=document)
        document_out = response.document
        # Normalize output into a simple list of key‑value structures
        fields = []
        for entity in document_out.entities:
            kv = {'key': None, 'value': None}
            # Simple heuristic: treat first child as key, second as value
            if entity.properties:
                kv['key'] = entity.properties[0].text or ''
                if len(entity.properties) > 1:
                    kv['value'] = entity.properties[1].text or ''
            # Add tables separately
            if entity.type_ == ga_docai.Document.Type.TABLE:
                # Placeholder – in a real implementation you would iterate over table cells
                kv['key'] = 'TABLE_SECTION'
                kv['value'] = 'TABLE_CONTENTS'
            fields.append(kv)
        return fields
