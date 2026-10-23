from google.cloud import language_v1 as language
import os


class ScriptSafetyChecker:
    def __init__(self):
        self.client = language.LanguageServiceClient()

    def check_safety(self, text: str) -> dict:
        document = language.Document(
            content=text, type_=language.Document.Type.PLAIN_TEXT
        )
        response = self.client.analyze_sentiment(request={"document": document})

        sentiment = response.document_sentiment

        response = self.client.moderate_text(request={"document": document})

        return {
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "toxicity": response.moderation_categories[0].confidence,
            "insult": response.moderation_categories[6].confidence,
        }
