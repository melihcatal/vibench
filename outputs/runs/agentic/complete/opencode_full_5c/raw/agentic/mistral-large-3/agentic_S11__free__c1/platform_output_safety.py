from typing import Dict, Any
from model_models import ModelResponse
from google.cloud import language_v1


def platform_output_safety(response: ModelResponse) -> Dict[str, Any]:
    """Checks Azure AI Inference model output for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=response.content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment.score

    # Google Cloud's Content Safety API (hypothetical for this example)
    safety_response = client.moderate_text(request={"document": document})

    return {
        "is_safe": safety_response.moderation_result.blocked == False,
        "safety_categories": [
            cat.name for cat in safety_response.moderation_result.categories
        ],
        "sentiment_score": sentiment,
        "provider": "google-cloud-natural-language",
    }
