class DocumentRequest:
    def __init__(self, image_path):
        self.image_path = image_path


class DocumentResponse:
    def __init__(self, blocks):
        self.blocks = blocks


def normalize_response(response):
    return DocumentResponse(response["Blocks"])
