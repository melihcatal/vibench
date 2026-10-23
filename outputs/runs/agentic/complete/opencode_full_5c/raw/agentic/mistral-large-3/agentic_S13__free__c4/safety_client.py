from typing import Dict, List, Optional
import os
from google.cloud import language_v1
from google.cloud.language_v1 import types


class TextModerationClient:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}"

    def analyze_content(self, text: str) -> types.AnalyzeEntitySentimentResponse:
        document = types.Document(content=text, type_=types.Document.Type.PLAIN_TEXT)
        return self.client.analyze_entity_sentiment(
            request={"parent": self.parent, "document": document}
        )

    def moderate_text(self, text: str) -> Dict:
        response = self.analyze_content(text)
        return {
            "entities": [
                {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "sentiment": {
                        "score": entity.sentiment.score,
                        "magnitude": entity.sentiment.magnitude,
                    },
                }
                for entity in response.entities
            ],
            "language": response.language,
        }
