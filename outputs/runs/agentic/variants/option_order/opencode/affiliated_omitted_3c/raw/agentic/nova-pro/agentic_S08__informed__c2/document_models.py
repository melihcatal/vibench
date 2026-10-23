class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, entities):
        self.entities = entities


def normalize_response(response):
    return {
        "vendor": response.entities[0].mention_text,
        "date": response.entities[1].mention_text,
        "total": response.entities[2].mention_text,
        "line_items": [entity.mention_text for entity in response.entities[3:]],
    }
