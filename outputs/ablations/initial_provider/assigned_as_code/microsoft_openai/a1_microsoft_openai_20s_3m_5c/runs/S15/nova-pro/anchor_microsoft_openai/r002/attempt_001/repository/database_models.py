class DocumentRequest:
    def __init__(self, id, document):
        self.id = id
        self.document = document

class DocumentResponse:
    def __init__(self, document):
        self.document = document

def normalize_document(document):
    return dict(document)