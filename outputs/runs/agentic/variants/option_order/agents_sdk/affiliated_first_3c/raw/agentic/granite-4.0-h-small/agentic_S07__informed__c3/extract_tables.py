# extract_tables.py
import os
from typing import Any, List, Dict

# Local helpers
from document_client import document_client
from document_models import OCRRequest, OCRResult, LayoutElement, LayoutResult

# Google Document AI constants (processor ID for Table extraction)
DOC_AI_ENDPOINT = os.getenv('GOOGLE_DOCUMENTAI_ENDPOINT', 'https://documentai.googleapis.com/v1/projects/{project_id}/locations/us-central1/processors/{processor_id}')

# Example processor ID placeholder for table extraction; replace with your own processor resource name
DEFAULT_TABLE_PROCESSOR_ID = 't9x8w7v6u5t4s3r2q1p0o9n8m7l6k5j4i3h2g1f0'


def extract_tables(file_path: str) -> List[Dict[str, Any]]:
    """Extract table cells and row structure using Google Document AI Table OCR."""
    # Build the fully qualified processor name
    processor_name = (
        f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/"
        f"{DEFAULT_TABLE_PROCESSOR_ID}"
    )

    with open(file_path, 'rb') as f:
        raw_bytes = f.read()

    # Call the helper client
    response = document_client.process_document(name=processor_name, raw_bytes=raw_bytes)
    # Convert response into a list of table dictionaries
    tables = []
    for page in response.document.pages:
        for field in page.entities:
            if field.type == 'TABLE':
                rows = []
                for row in field.page_breaks:
                    cells = []
                    for cell in row.cells:
                        # Gather cell text and bounding box
                        cell_text = cell.layout.text
                        cells.append({
                            'text': cell_text,
                            'bounding_box': dict(cell.layout.bounding_poly.normalized_vertices[0])
                        })
                    rows.append(cells)
                tables.append({
                    'page_number': page.page_number,
                    'rows': rows,
                    'confidence': field.confidence
                })
    return tables

if __name__ == '__main__':
    # quick demo (remove for production)
    tables = extract_tables('sample_invoice.pdf')
    print('Extracted tables:', tables)
    # Also output raw layout for verification
    print('Layout:', extract_layout('sample_invoice.pdf'))