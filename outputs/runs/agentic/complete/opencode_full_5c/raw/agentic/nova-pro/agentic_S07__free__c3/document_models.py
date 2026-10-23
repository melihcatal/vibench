class DocumentRequest:
    def __init__(self, document):
        self.document = document


class DocumentResponse:
    def __init__(self, response):
        self.response = response


def normalize_response(response):
    return DocumentResponse(response)
