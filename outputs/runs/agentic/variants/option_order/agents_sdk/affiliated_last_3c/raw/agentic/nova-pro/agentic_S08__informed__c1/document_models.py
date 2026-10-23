class Invoice:
    def __init__(self, vendor, date, total, items):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.items = items

class Receipt:
    def __init__(self, merchant, tax, total, items):
        self.merchant = merchant
        self.tax = tax
        self.total = total
        self.items = items