class VisionModel:
    def __init__(self, client):
        self.client = client
    def normalize_response(self, response):
        return [item['description'] for item in response]
