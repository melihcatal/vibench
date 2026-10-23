def extract_plain_text(result: dict) -> str:
    paragraphs = result.get('paragraphs', [])
    return '\n'.join([p.get('content', '') for p in paragraphs]).strip()

def extract_layout_elements(result: dict) -> dict:
    return {
        'paragraphs': result.get('paragraphs', []),
        'tables': result.get('tables', []),
        'pages': result.get('pages', [])
    }

def extract_tables(result: dict) -> list:
    return result.get('tables', [])

def extract_key_values(result: dict) -> dict:
    kv_dict = {}
    # From keyValuePairs
    kv_pairs = result.get('keyValuePairs', [])
    for kvp in kv_pairs:
        key_content = kvp.get('key', {}).get('content')
        value_content = kvp.get('value', {}).get('content')
        if key_content and value_content:
            kv_dict[key_content] = value_content
    # From fields in documents
    documents = result.get('documents', [])
    if documents:
        fields = documents[0].get('fields', {})
        for field_name, field_value in fields.items():
            content = field_value.get('content')
            if content:
                kv_dict[field_name] = content
    return kv_dict