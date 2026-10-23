import os
from google.cloud import vision
from google.oauth2 import service_account

# Load credentials from env var
credentials = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

class VisionClient:
    def __init__(self, vision=vision_client):
        self.vision = vision
    
    def detect_labels(self, image_path):
        with open(image_path, 'rb') as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.vision.annotate_image({'image': image, 'features': [{'type_': vision.Feature.Type.LABEL_DETECTION}]})
        labels = [item.description for item in response.label_annotations]
        return labels
    
    def describe_image(self, image_path):
        with open(image_path, 'rb') as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.vision.annotate_image({'image': image, 'features': [{'type_': vision.Feature.Type.IMAGE_PROPERTIES}]})
        description = response.image_properties.description
        return description
    
    def detect_text(self, image_path):
        with open(image_path, 'rb') as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.vision.annotate_image({'image': image, 'features': [{'type_': vision.Feature.Type.TEXT_DETECTION}]})
        texts = [text.description for text in response.text_annotations]
        return texts
    
    def score_safety(self, image_path):
        with open(image_path, 'rb') as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.vision.annotate_image({'image': image, 'features': [{'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION}]})
        safe = response.safe_search_annotation
        return safe.adult == 'VERY_UNLIKELY' and safe.violence == 'VERY_UNLIKELY' and safe.racy == 'VERY_UNLIKELY'
