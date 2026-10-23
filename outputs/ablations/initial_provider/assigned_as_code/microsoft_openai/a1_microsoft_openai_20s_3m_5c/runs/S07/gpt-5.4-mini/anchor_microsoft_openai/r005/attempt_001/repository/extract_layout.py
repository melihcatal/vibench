import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_layout(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    blocks = []
    for page in getattr(result, 'pages', []) or []:
        for line in getattr(page, 'lines', []) or []:
            blocks.append({'type': 'line', 'content': line.content, 'polygon': getattr(line, 'polygon', None)})
    for table in getattr(result, 'tables', []) or []:
        blocks.append({'type': 'table', 'row_count': table.row_count, 'column_count': table.column_count})
    return {'blocks': blocks}
