import os
from typing import Dict, Any
from google.cloud import language_v1

# Google Cloud Natural Language API Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")


def moderate_claims(text: str) -> Dict[str, Any]:
    """Moderate free-text claims using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_sentiment(request={"document": document})

    # Check for toxic content
    toxicity_client = language_v1.LanguageServiceClient()
    toxicity_response = toxicity_client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "model": "projects/{GCP_PROJECT_ID}/locations/global/models/toxicity"
            },
        }
    )

    return {
        "sentiment": {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        },
        "toxicity": {
            "categories": [
                {
                    "name": category.name,
                    "confidence": category.confidence,
                }
                for category in toxicity_response.categories
            ]
        },
    }
