class VisionRequest:
    def __init__(self, image_path):
        self.image_path = image_path

class VisionResponse:
    def __init__(self, response):
        self.response = response

def normalize_response(response):
    return response