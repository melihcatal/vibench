import os
import json

class VisionClient:
    """Simple wrapper that instantiates provider-specific SDK clients.
    The `service` parameter selects the concrete provider.
    "]"""
    def __init__(self, service):
        if service == 'rekognition':
            import boto3
            self.client = boto3.client('rekognition')
        elif service == 'vision':
            # Azure AI Vision / Google Vision have similar SDK signatures
            from azure.ai.vision import ImageAnalysisClient
            endpoint = os.getenv('AZURE_VISION_ENDPOINT')
            key = os.getenv('AZURE_VISION_KEY')
            self.client = ImageAnalysisClient(endpoint=endpoint, credential=key)
        elif service == 'vision_google':
            from google.cloud import vision
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            self.client = vision.ImageAnnotatorClient()
        else:
            raise ValueError(f'Unsupported service: {service}')

    def detect_labels(self, Image):
        return self.client.detect_labels(Image=Image)

    def describe_image(self, Image):
        return self.client.describe_image(Image=Image)

    def text_detection(self, Image):
        return self.client.text_detection(Image=Image)

    def detect_moderation_labels(self, Image):
        return self.client.detect_moderation_labels(Image=Image)
