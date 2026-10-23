class DocumentRequest:
    def __init__(self, content, mime_type):
        self.content = content
        self.mime_type = mime_type


class DocumentResponse:
    def __init__(self, fields):
        self.fields = fields


class NormalizedExpense:
    def __init__(self, vendor, date, total, line_items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items
