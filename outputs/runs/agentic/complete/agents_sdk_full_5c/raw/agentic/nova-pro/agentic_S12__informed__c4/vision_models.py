class VisionModel:
    def __init__(self, client):
        self.client = client

    def detect_labels(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.client.detect_labels(Image={'Bytes': image.read()})
        return response['Labels']

    def detect_text(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.client.detect_text(Image={'Bytes': image.read()})
        return response['TextDetections']

    def score_safety(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.client.detect_moderation_labels(Image={'Bytes': image.read()})
        return response['ModerationLabels']