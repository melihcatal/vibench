class DocumentModel:
    def __init__(self, text, entities, tables):
        self.text = text
        self.entities = entities
        self.tables = tables