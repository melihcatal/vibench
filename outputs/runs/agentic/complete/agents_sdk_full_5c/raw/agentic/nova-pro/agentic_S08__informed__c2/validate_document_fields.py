from google.cloud import documentai

def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in document:
            return False
    return True