def summarize_document(document):
    return {k: v for k, v in document.items() if k in ['id', 'title', 'author']}