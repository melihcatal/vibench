class OCRResponse:
    def __init__(self, text, layout, tables, keyValues):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.keyValues = keyValues