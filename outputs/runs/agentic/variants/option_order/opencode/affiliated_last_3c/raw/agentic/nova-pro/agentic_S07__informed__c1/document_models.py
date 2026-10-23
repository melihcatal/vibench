class OCRResponse:
    def __init__(self, text):
        self.text = text


class LayoutResponse:
    def __init__(self, layout):
        self.layout = layout


class TablesResponse:
    def __init__(self, tables):
        self.tables = tables


class KeyValuesResponse:
    def __init__(self, key_values):
        self.key_values = key_values
