import json

def normalize_document(document):
    return {'id': {'S': document.get('id')}, 'document': {'S': json.dumps(document)}}