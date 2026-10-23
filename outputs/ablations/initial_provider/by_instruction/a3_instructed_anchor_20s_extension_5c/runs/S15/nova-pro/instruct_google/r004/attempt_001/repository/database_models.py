def normalize_document(document):
    return {k: v for k, v in document.items() if not k.startswith('__')}