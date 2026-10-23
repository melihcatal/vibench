def summarize_document(document):
    summary = {k: v for k, v in document.items() if k in ['title', 'description']}
    return summary