# extract_key_values.py
import os
from typing import Any, List, Dict

# Local helpers
from document_client import document_client
from document_models import OCRRequest, OCRResult, LayoutElement, LayoutResult

# Google Document AI constants (processor ID for Key-Value extraction)
DOC_AI_ENDPOINT = os.getenv('GOOGLE_DOCUMENTAI_ENDPOINT', 'https://documentai.googleapis.com/v1/projects/{project_id}/locations/us-central1/processors/{processor_id}')

# Example processor ID for a generic form; replace with your own
DEFAULT_KV_PROCESSOR_ID = 'k1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9'


def extract_key_values(file_path: str) -> List[Dict[str, Any]]:
    """Extract key‑value pairs from a form‑like document using Google Document AI.
    Returns a list of dictionaries, each representing a field with 'key' and 'value'.
    """
    # Build the fully qualified processor name
    processor_name = (
        f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/"
        f"{DEFAULT_KV_PROCESSOR_ID}"
    )

    with open(file_path, 'rb') as f:
        raw_bytes = f.read()

    # Call the Document AI client (via our helper)
    response = document_client.process_document(name=processor_name, raw_bytes=raw_bytes)
    kv_pairs = []
    # The response payload class varies by processor; the following works for the generic Form OCR
    for page in response.document.pages:
        for field in page.entities:
            # Look for Key‑Value entities; adjust if your processor uses a different type.
            if field.type == 'KEY_VALUE_SET':
                # A KV set contains a 'key' and a 'value' sub‑entity
                kv_field = {'page_number': page.page_number}
                for sub in field.properties:
                    if sub.type == 'KEY':
                        kv_field['key'] = sub.name
                    elif sub.type == 'VALUE':
                        kv_field['value'] = sub.name
                if 'key' in kv_field and 'value' in kv_field:
                    kv_pairs.append(kv_field)
    return kv_pairs

if __name__ == '__main__':
    # Simple demo (remove before shipping)
    form_fields = extract_key_values('sample_form.jpg')
    print('Extracted KV pairs:', form_fields)
    # Optionally show layout together
    print('Layout preview:', extract_layout('sample_form.jpg'))