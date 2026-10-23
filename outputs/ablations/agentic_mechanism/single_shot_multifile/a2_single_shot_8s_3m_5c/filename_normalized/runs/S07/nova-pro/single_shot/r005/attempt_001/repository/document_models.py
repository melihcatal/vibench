class DocumentRequest:
    def __init__(self, image_path):
        with open(image_path, 'rb') as image:
            self.bytes = image.read()

class DocumentResponse:
    def __init__(self, response):
        self.blocks = response['Blocks']