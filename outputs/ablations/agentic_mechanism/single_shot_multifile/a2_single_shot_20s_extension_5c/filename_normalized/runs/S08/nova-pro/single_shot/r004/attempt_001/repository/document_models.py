class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path

class DocumentResponse:
    def __init__(self, data):
        self.data = data

class NormalizedExpense:
    def __init__(self, expense):
        self.expense = expense