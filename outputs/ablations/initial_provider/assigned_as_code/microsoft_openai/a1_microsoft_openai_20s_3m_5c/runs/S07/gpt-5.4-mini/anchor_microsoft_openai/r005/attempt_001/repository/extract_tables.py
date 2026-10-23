import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_tables(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    tables = []
    for table in getattr(result, 'tables', []) or []:
        cells = []
        for cell in getattr(table, 'cells', []) or []:
            cells.append({'row_index': cell.row_index, 'column_index': cell.column_index, 'content': cell.content, 'row_span': getattr(cell, 'row_span', 1), 'column_span': getattr(cell, 'column_span', 1)})
        tables.append({'row_count': table.row_count, 'column_count': table.column_count, 'cells': cells})
    return {'tables': tables}
