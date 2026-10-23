from typing import Dict, List, Optional
import os
from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPICallError


class SafetyClient:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    def analyze_text(self, text: str) -> Optional[Dict]:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        try:
            response = self.client.analyze_sentiment(request={"document": document})
            return {
                "sentiment": {
                    "score": response.document_sentiment.score,
                    "magnitude": response.document_sentiment.magnitude,
                },
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
            }
        except GoogleAPICallError as e:
            print(f"Google API call failed: {e}")
            return None

    def moderate_text_content(self, text: str) -> Optional[Dict]:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        try:
            response = self.client.moderate_text(
                request={
                    "document": document,
                    "moderation_config": {
                        "category_scores": True,
                        "hate_speech": True,
                        "dangerous_content": True,
                        "harassment": True,
                        "sexually_explicit": True,
                    },
                }
            )
            return {
                "moderation_scores": {
                    "hate_speech": response.moderation_scores.hate_speech,
                    "dangerous_content": response.moderation_scores.dangerous_content,
                    "harassment": response.moderation_scores.harassment,
                    "sexually_explicit": response.moderation_scores.sexually_explicit,
                },
                "language": response.language,
            }
        except GoogleAPICallError as e:
            print(f"Google API call failed: {e}")
            return None
