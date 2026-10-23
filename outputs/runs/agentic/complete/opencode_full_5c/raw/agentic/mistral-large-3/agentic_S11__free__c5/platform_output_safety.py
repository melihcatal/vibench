from typing import Dict, Any
from model_models import ChatResponse
from google.cloud import language_v1


def platform_output_safety(response: ChatResponse) -> Dict[str, Any]:
    """
    Checks Azure AI Inference model output for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=response.content,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    safety_check = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_unsafe": sentiment.score < -0.5 or sentiment.magnitude > 0.8,
        "categories": [],
    }

    return safety_check
