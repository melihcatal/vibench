class DocumentRequest:
    def __init__(self, document):
        self.document = document


class DocumentResponse:
    def __init__(self, text, layout, tables, key_value_pairs):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_value_pairs = key_value_pairs
