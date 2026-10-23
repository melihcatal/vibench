from google.cloud import vision_v1
from google.cloud import translate_v2 as translate
from google.cloud import storage
from google.cloud import language_v1


class VisionClient:
    def __init__(self):
        self.image_annotator_client = vision_v1.ImageAnnotatorClient()
        self.translate_client = translate.Client()
        self.storage_client = storage.Client()
        self.language_client = language_v1.LanguageServiceClient()
