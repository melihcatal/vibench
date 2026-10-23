import os
from typing import Optional
from google.cloud import documentai


def get_document_ai_client():
    return documentai.DocumentProcessorServiceClient()


def get_processor_name(project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None):
    project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = location or os.environ.get('DOCUMENT_AI_LOCATION', 'us')
    processor_id = processor_id or os.environ.get('DOCUMENT_AI_PROCESSOR_ID')
    if not project_id or not processor_id:
        raise ValueError('Missing project_id or processor_id')
    return f'projects/{project_id}/locations/{location}/processors/{processor_id}'


def load_document_bytes(document_path: str) -> bytes:
    with open(document_path, 'rb') as f:
        return f.read()


def detect_mime_type(document_path: str) -> str:
    lower = document_path.lower()
    if lower.endswith('.pdf'):
        return 'application/pdf'
    if lower.endswith('.png'):
        return 'image/png'
    if lower.endswith('.jpg') or lower.endswith('.jpeg'):
        return 'image/jpeg'
    return 'application/octet-stream'


def _get_text(entity):
    if hasattr(entity, 'normalized_value') and entity.normalized_value.text:
        return entity.normalized_value.text
    return entity.mention_text or ''


def normalize_text_response(document):
    return {'text': document.text or '', 'pages': len(document.pages)}


def normalize_layout_response(document):
    blocks = []
    for page_index, page in enumerate(document.pages):
        for block in page.blocks:
            blocks.append({'page': page_index + 1, 'layout': 'block', 'text': _get_text(block.layout), 'confidence': block.layout.confidence})
        for line in page.lines:
            blocks.append({'page': page_index + 1, 'layout': 'line', 'text': _get_text(line.layout), 'confidence': line.layout.confidence})
        for token in page.tokens:
            blocks.append({'page': page_index + 1, 'layout': 'token', 'text': _get_text(token.layout), 'confidence': token.layout.confidence})
    return {'elements': blocks, 'text': document.text or ''}


def normalize_table_response(document):
    tables = []
    for page_index, page in enumerate(document.pages):
        for table in page.tables:
            rows = []
            for row in table.header_rows + table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append({'text': _get_text(cell.layout), 'row_span': cell.row_span, 'col_span': cell.col_span})
                rows.append(cells)
            tables.append({'page': page_index + 1, 'rows': rows})
    return {'tables': tables}


def normalize_kv_response(document):
    pairs = []
    for entity in document.entities:
        if entity.type_:
            pairs.append({'key': entity.type_, 'value': _get_text(entity)})
    return {'key_values': pairs, 'text': document.text or ''}
