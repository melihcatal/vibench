class DocumentModel:
    def __init__(self, document):
        self.document = document

    def to_bytes(self):
        return self.document