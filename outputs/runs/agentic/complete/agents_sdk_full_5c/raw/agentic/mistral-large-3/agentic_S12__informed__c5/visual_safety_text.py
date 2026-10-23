import requests
from typing import List
from vision_models import LabelDetectionResponse

class PerspectiveAPI:
    def __init__(self):
        self.api_key = "PERSPECTIVE_API_KEY"
        self.url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.api_key}"

    def check_text_safety(self, texts: List[str]) -> bool:
        for text in texts:
            data = {
                "comment": {"text": text},
                "requestedAttributes": {"TOXICITY": {}}
            }
            response = requests.post(self.url, json=data)
            response.raise_for_status()
            toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            if toxicity_score > 0.7:
                return False
        return True

def visual_safety_text(labels: LabelDetectionResponse) -> bool:
    perspective = PerspectiveAPI()
    return perspective.check_text_safety(labels.labels)