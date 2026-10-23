import os

VISION_API_KEY = os.getenv('VISION_API_KEY')

class VisionClient:
    def __init__(self):
        self.base_url = 'https://vision.googleapis.com/v1/images:annotate?key=' + VISION_API_KEY

    def annotate(self, image_data, feature):
        response = requests.post(
            self.base_url,
            json={
                'requests': [{
                    'image': {'content': image_data},
                    'features': [{'type': feature}]
                }]
            }
        )
        return response.json()['responses'][0]