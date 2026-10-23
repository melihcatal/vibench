import os
import requests
from document_models import DocumentResponse

class OCRChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def is_safe(self, text: str) -> bool:
        payload = {
            "comment": {
                "text": text
            },
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {}
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        resp = requests.post(self.endpoint, json=payload, headers=headers, params={"key": self.api_key})
        resp.raise_for_status()
        result = resp.json()
        score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        # Consider safe if toxicity score is below 0.5
        return score < 0.5

    def check_document(self, doc: DocumentResponse) -> bool:
        return self.is_safe(doc["text"])

if __name__ == "__main__":
    from extract_text import ExtractText
    extractor = ExtractText()
    doc = extractor.extract("sample.jpg")
    checker = OCRChecker()
    print(checker.check_document(doc))
