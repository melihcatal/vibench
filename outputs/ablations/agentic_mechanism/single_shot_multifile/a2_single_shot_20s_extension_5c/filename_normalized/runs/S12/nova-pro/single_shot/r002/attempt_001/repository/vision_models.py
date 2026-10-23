class VisionRequest:
    def __init__(self, image_path, feature_type):
        self.image_path = image_path
        self.feature_type = feature_type

    def to_payload(self):
        return {
            'requests': [{
                'image': {'content': open(self.image_path, 'rb').read().decode('utf-8')},
                'features': [{'type': self.feature_type}]
            }]
        }

class VisionResponse:
    def __init__(self, response_json):
        self.response_json = response_json

    def get_labels(self):
        return self.response_json['responses'][0]['labelAnnotations']

    def get_text(self):
        return self.response_json['responses'][0]['fullTextAnnotation']['text']

    def get_safety(self):
        return self.response_json['responses'][0]['safeSearchAnnotation']