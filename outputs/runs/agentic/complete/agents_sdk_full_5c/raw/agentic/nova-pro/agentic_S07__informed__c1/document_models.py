class DocumentModel:
    def __init__(self, text, layout, tables, key_values):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_values = key_values