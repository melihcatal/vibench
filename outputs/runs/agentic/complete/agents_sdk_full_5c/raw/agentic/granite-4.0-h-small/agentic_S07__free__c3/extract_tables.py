import os
import requests
from document_models import OCRResponse

def table_from_gcp_response(payload: dict) -> List[TableSpec]:
    """Convert GCP Document AI tabular structure to our TableSpec model.
    """
    tables = []
    for entity in payload.get('pages', [{}])[0].get('tables', []):
        headers = [col['text'] for col in entity.get('headerRows', [])]
        rows = []
        for row in entity.get('rows', []):
            rows.append([col['text'] for col in row['cells']])
        tables.append(TableSpec(column_headers=headers, rows=rows))
    return tables

# Example usage (not executed here)
# tables = table_from_gcp_response(gcp_payload)
