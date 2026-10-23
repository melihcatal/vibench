from google.cloud import vision


class VisionClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def get_client(self):
        return self.client
