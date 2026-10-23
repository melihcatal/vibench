class ExtractedFields:
    def __init__(self, vendor=None, date=None, total=None, line_items=None):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items if line_items is not None else []

class NormalizedExpense:
    def __init__(self, vendor=None, date=None, total=None, line_items=None):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items if line_items is not None else []