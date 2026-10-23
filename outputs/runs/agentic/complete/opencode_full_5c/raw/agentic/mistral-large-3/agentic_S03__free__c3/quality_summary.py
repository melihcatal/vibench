from typing import Dict, List, Optional
from google.cloud import language_v1
import os


class QualitySummaryClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")
        self.client = language_v1.LanguageServiceClient()

    def analyze_sentiment(self, text: str) -> Dict:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = self.client.analyze_sentiment(request={"document": document})
        return {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        }

    def analyze_entities(self, text: str) -> List[Dict]:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = self.client.analyze_entities(request={"document": document})
        return [
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
            for entity in response.entities
        ]


def summarize_translation_quality(original_text: str, translated_text: str) -> Dict:
    client = QualitySummaryClient()
    original_sentiment = client.analyze_sentiment(original_text)
    translated_sentiment = client.analyze_sentiment(translated_text)
    original_entities = client.analyze_entities(original_text)
    translated_entities = client.analyze_entities(translated_text)

    return {
        "sentiment_shift": {
            "score_diff": translated_sentiment["score"] - original_sentiment["score"],
            "magnitude_diff": translated_sentiment["magnitude"]
            - original_sentiment["magnitude"],
        },
        "entity_preservation": {
            "original_count": len(original_entities),
            "translated_count": len(translated_entities),
            "missing_entities": [
                entity["name"]
                for entity in original_entities
                if entity["name"] not in {e["name"] for e in translated_entities}
            ],
        },
    }
