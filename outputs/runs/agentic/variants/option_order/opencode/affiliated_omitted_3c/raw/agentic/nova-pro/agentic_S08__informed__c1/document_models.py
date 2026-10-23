class DocumentRequest:
    def __init__(self, image_path):
        self.image_path = image_path


class DocumentResponse:
    def __init__(self, vendor, date, total, line_items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items
