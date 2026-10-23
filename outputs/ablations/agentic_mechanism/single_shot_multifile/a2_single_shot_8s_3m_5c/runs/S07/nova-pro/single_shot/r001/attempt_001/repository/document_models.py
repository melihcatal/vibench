class OCRResponse:
    def __init__(self, response):
        self.text = self.extract_text(response)
        self.layout = self.extract_layout(response)
        self.tables = self.extract_tables(response)
        self.keyValues = self.extract_key_values(response)

    def extract_text(self, response):
        pass  # Implement text extraction

    def extract_layout(self, response):
        pass  # Implement layout extraction

    def extract_tables(self, response):
        pass  # Implement table extraction

    def extract_key_values(self, response):
        pass  # Implement key-value extraction