import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import normalize_payload


def extract_tables(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    tables = []
    for table in getattr(result, 'tables', []):
        cells = []
        for cell in getattr(table, 'cells', []):
            cells.append(cell.to_dict() if hasattr(cell, 'to_dict') else cell)
        tables.append({'row_count': getattr(table, 'row_count', None), 'column_count': getattr(table, 'column_count', None), 'cells': cells})
    return {'tables': tables}
