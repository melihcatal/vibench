import boto3

class VisionClient:
    def __init__(self):
        self.rekognition_client = boto3.client('rekognition')

    def detect_labels(self, image_bytes):
        response = self.rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10
        )
        return response

    def detect_text(self, image_bytes):
        response = self.rekognition_client.detect_text(
            Image={'Bytes': image_bytes}
        )
        return response

    def moderate_content(self, image_bytes):
        response = self.rekognition_client.detect_moderation_labels(
            Image={'Bytes': image_bytes}
        )
        return response

    def describe_image(self, image_bytes):
        response = self.rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=1
        )
        return response['Labels'][0]['Name'] if response['Labels'] else 'No description found'
