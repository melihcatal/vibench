class DocumentResponse:
    def __init__(self, response):
        self.response = response

    def get_text(self):
        return [
            item["Text"]
            for item in self.response["Blocks"]
            if item["BlockType"] == "LINE"
        ]

    def get_layout(self):
        return [
            item
            for item in self.response["Blocks"]
            if item["BlockType"] in ["TABLE", "CELL"]
        ]

    def get_tables(self):
        return [
            item for item in self.response["Blocks"] if item["BlockType"] == "TABLE"
        ]

    def get_key_values(self):
        return [
            item
            for item in self.response["Blocks"]
            if item["BlockType"] == "KEY_VALUE_PAIR"
        ]
