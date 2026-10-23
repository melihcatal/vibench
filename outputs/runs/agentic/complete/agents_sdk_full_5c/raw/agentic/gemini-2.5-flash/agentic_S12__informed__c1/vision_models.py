import base64
from typing import List, Dict, Any

class ImageInput:
    def __init__(self, image_content_base64: str):
        self.image_content_base64 = image_content_base64

class ImageLabel:
    def __init__(self, description: str, score: float):
        self.description = description
        self.score = score

class ImageText:
    def __init__(self, text: str, bounds: List[Dict[str, int]]):
        self.text = text
        self.bounds = bounds

class ImageSafeSearchAnnotation:
    def __init__(self, adult: str, spoof: str, medical: str, violence: str, racy: str):
        self.adult = adult
        self.spoof = spoof
        self.medical = medical
        self.violence = violence
        self.racy = racy

class ImageDescription:
    def __init__(self, description: str):
        self.description = description
