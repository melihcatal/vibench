import base64


def normalize_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint'),
        'api_key': config.get('api_key'),
        'source_language': config.get('source_language', 'en'),
        'target_language': config.get('target_language', 'en'),
        'model_id': config.get('model_id', 'text-embedding-3-small'),
        'safety_threshold': config.get('safety_threshold', 0.5),
    }


def normalize_payload(payload):
    payload = payload or {}
    result = dict(payload)
    if 'document_bytes' not in result and 'document_base64' in result:
        result['document_bytes'] = base64.b64decode(result['document_base64'])
    if 'mime_type' not in result:
        result['mime_type'] = 'image/png'
    return result


def extract_content(result):
    if isinstance(result, dict):
        return result.get('content') or result.get('text') or ''
    return getattr(result, 'content', '')


def extract_tables(result):
    tables = []
    for table in getattr(result, 'tables', []) or []:
        cells = []
        for cell in getattr(table, 'cells', []) or []:
            cells.append({
                'row_index': getattr(cell, 'row_index', None),
                'column_index': getattr(cell, 'column_index', None),
                'content': getattr(cell, 'content', ''),
                'kind': getattr(cell, 'kind', None),
            })
        tables.append({
            'row_count': getattr(table, 'row_count', None),
            'column_count': getattr(table, 'column_count', None),
            'cells': cells,
        })
    return tables


def extract_key_values(result):
    pairs = []
    for field in getattr(result, 'key_value_pairs', []) or []:
        key = getattr(getattr(field, 'key', None), 'content', '')
        value = getattr(getattr(field, 'value', None), 'content', '')
        pairs.append({'key': key, 'value': value})
    return pairs


def extract_layout(result):
    blocks = []
    for paragraph in getattr(result, 'paragraphs', []) or []:
        blocks.append({'kind': 'paragraph', 'content': getattr(paragraph, 'content', '')})
    for table in getattr(result, 'tables', []) or []:
        blocks.append({'kind': 'table', 'cells': extract_tables(type('R', (), {'tables': [table]})())})
    return blocks
