class DocumentRequest:
    def __init__(self, bucket, name):
        self.bucket = bucket
        self.name = name

class DocumentResponse:
    def __init__(self, data):
        self.data = data

class NormalizedExpense:
    def __init__(self, vendor, date, total, items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.items = items