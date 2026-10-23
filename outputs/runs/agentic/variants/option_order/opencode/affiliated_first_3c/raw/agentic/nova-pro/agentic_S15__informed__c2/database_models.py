class Document:
    def __init__(self, primary_key, data):
        self.primary_key = primary_key
        self.data = data

    def to_dict(self):
        return {self.primary_key: self.data}
