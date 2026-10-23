class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def from_dict(doc_dict):
        return Document(doc_dict['id'], doc_dict['data'])