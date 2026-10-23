import os
from google.cloud import language_v1

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

class LiveCaptionSafetyChecker:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def check_safety(self, text):
        if not text:
            return {"score": 0.0, "magnitude": 0.0, "is_unsafe": False}

        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_sentiment(request={'document': document}).document_sentiment

        is_unsafe = False
        # Example heuristic: if sentiment score is very negative and magnitude is high
        if sentiment.score < -0.5 and sentiment.magnitude > 1.0: 
            is_unsafe = True

        return {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
            "is_unsafe": is_unsafe
        }
