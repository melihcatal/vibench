class DocumentModel:
    def __init__(self, document):
        self.document = document

    def normalize_response(self, response):
        return response