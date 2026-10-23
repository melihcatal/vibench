class DocumentRequest:
    def __init__(self, gcs_source_uri):
        self.gcs_source_uri = gcs_source_uri

class DocumentResponse:
    def __init__(self, document):
        self.document = document
