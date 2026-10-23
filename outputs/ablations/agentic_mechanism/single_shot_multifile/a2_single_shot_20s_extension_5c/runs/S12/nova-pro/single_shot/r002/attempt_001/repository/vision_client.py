import os

VISION_API_KEY = os.getenv('VISION_API_KEY')

class VisionClient:
    def __init__(self):
        self.base_url = 'https://vision.googleapis.com/v1/images:annotate?key=' + VISION_API_KEY
        self.headers = {'Content-Type': 'application/json'}

    def send_request(self, payload):
        response = requests.post(self.base_url, json=payload, headers=self.headers)
        return response.json()