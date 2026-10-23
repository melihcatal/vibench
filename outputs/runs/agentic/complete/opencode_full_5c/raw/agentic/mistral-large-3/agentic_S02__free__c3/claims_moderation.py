import os
from typing import Dict, Any
from google.cloud import language_v1

# Using Google Cloud Natural Language API for moderation
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project")


def moderate_claims(text: str) -> Dict[str, Any]:
    """Moderates free-text claims using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(request={"document": document})

    return {
        "moderation_scores": {
            "toxic": response.moderation_result.toxic_score,
            "insult": response.moderation_result.insult_score,
            "profane": response.moderation_result.profane_score,
            "derogatory": response.moderation_result.derogatory_score,
            "sexual": response.moderation_result.sexual_score,
            "death_harm": response.moderation_result.death_harm_score,
        },
        "blocked": response.moderation_result.blocked,
    }
