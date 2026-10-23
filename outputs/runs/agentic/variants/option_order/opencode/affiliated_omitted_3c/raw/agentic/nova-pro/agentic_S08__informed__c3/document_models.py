class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, vendor, date, total, line_items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items


def normalize_response(response):
    return {
        "vendor": response.vendor,
        "date": response.date.strftime("%Y-%m-%d"),
        "total": response.total,
        "line_items": response.line_items,
    }
