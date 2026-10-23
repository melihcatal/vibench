from google.cloud import language_v1

class VisualSafetyTextRequest:
    def __init__(self, text: str):
        self.text = text

class VisualSafetyTextResponse:
    def __init__(self, is_safe: bool, sentiment_score: float):
        self.is_safe = is_safe
        self.sentiment_score = sentiment_score

def visual_safety_text(request: VisualSafetyTextRequest) -> VisualSafetyTextResponse:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=request.text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # For simplicity, let's consider a negative sentiment score as potentially unsafe.
    # Threshold can be adjusted based on requirements.
    is_safe = sentiment.score >= -0.2

    return VisualSafetyTextResponse(is_safe=is_safe, sentiment_score=sentiment.score)
