import requests
from typing import Dict, List
from vision_models import ImageSafetyResponse
from vision_client import get_clarifai_pat

class ClarifaiSafetyScorer:
    def __init__(self):
        self.pat = get_clarifai_pat()
        self.user_id = "clarifai"
        self.app_id = "main"
        self.model_id = "moderation-recognition"
        self.url = f"https://api.clarifai.com/v2/users/{self.user_id}/apps/{self.app_id}/models/{self.model_id}/outputs"

    def score_safety(self, image_bytes: bytes) -> ImageSafetyResponse:
        headers = {
            "Authorization": f"Key {self.pat}",
            "Content-Type": "application/json"
        }
        base64_image = image_bytes.hex() if isinstance(image_bytes, bytes) else image_bytes
        data = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "base64": base64_image
                        }
                    }
                }
            ]
        }
        response = requests.post(self.url, headers=headers, json=data)
        response.raise_for_status()
        concepts = response.json()["outputs"][0]["data"]["concepts"]
        unsafe_concepts = [c["name"] for c in concepts if c["value"] > 0.5]
        return ImageSafetyResponse(is_safe=not bool(unsafe_concepts), unsafe_concepts=unsafe_concepts)

def score_image_safety(image_bytes: bytes) -> ImageSafetyResponse:
    scorer = ClarifaiSafetyScorer()
    return scorer.score_safety(image_bytes)