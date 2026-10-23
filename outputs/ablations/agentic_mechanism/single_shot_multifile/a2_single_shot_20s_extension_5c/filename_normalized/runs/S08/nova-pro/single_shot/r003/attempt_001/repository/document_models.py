class DocumentRequest:
    def __init__(self, content, mime_type):
        self.content = content
        self.mime_type = mime_type

class DocumentResponse:
    def __init__(self, document):
        self.document = document

    def extract_fields(self):
        fields = {}
        for entity in self.document.entities:
            fields[entity.type_] = entity.mention_text
        return fields