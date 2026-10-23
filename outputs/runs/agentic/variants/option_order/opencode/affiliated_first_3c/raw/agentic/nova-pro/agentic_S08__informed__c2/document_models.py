class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, data):
        self.data = data


class NormalizedExpense:
    def __init__(self, vendor, date, total, line_items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items
