from fetch_document import fetch_document

def summarize_record(table_name, document_id):
    document = fetch_document(table_name, document_id)
    if document:
        return f'Document {document_id} summary: {document.get(