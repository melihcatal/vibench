import boto3

class VisionClient:
    def __init__(self):
        self.rekognition_client = boto3.client('rekognition')

    def detect_labels(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.rekognition_client.detect_labels(Image={'Bytes': image.read()})
        return response

    def describe_image(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.rekognition_client.detect_labels(Image={'Bytes': image.read()})
        return {'Description': ' '.join([label['Name'] for label in response['Labels']])}

    def detect_text(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.rekognition_client.detect_text(Image={'Bytes': image.read()})
        return response

    def check_safety(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.rekognition_client.detect_moderation_labels(Image={'Bytes': image.read()})
        return response