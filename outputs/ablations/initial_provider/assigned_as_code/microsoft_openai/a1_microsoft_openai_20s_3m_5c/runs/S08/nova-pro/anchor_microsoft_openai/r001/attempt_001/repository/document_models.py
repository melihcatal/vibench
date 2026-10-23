class DocumentRequest:
    def __init__(self, document_bytes, mime_type):
        self.document_bytes = document_bytes
        self.mime_type = mime_type


class DocumentResponse:
    def __init__(self, documents):
        self.documents = documents


class NormalizedExpense:
    def __init__(self, vendor, date, total, line_items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items