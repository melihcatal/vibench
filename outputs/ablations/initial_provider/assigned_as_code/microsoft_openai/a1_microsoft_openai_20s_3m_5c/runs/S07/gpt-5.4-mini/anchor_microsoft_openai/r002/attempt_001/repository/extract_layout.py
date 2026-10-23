import io
from document_client import make_client


def extract_layout(payload, config=None):
    with make_client(config) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'layout': {'pages': getattr(result, 'pages', None), 'paragraphs': getattr(result, 'paragraphs', None), 'tables': getattr(result, 'tables', None)}}
