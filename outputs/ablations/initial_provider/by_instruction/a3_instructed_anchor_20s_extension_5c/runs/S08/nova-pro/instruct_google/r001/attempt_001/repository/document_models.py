class DocumentRequest:
    def __init__(self, image_path):
        self.image_path = image_path

class DocumentResponse:
    def __init__(self, text):
        self.text = text