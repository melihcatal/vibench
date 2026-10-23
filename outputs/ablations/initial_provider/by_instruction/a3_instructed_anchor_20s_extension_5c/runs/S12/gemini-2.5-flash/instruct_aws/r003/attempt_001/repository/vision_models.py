from typing import List, Dict, Any

class ImageLabel:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence

    def to_dict(self):
        return {"name": self.name, "confidence": self.confidence}

class ImageDescription:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {"description": self.text}

class ImageTextAnnotation:
    def __init__(self, description: str, bounding_poly: Dict):
        self.description = description
        self.bounding_poly = bounding_poly

    def to_dict(self):
        return {"description": self.description, "bounding_poly": self.bounding_poly}

class ImageSafetyScore:
    def __init__(self, is_racy: bool, adult_score: float, racy_score: float):
        self.is_racy = is_racy
        self.adult_score = adult_score
        self.racy_score = racy_score

    def to_dict(self):
        return {"is_racy": self.is_racy, "adult_score": self.adult_score, "racy_score": self.racy_score}

