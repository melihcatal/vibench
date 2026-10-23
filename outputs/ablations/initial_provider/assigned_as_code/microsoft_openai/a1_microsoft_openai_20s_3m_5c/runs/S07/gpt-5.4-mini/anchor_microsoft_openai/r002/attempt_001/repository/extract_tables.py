import io
from document_client import make_client


def extract_tables(payload, config=None):
    with make_client(config) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'tables': [{'row_count': getattr(table, 'row_count', None), 'column_count': getattr(table, 'column_count', None), 'cells': getattr(table, 'cells', None)} for table in getattr(result, 'tables', []) or []]}
