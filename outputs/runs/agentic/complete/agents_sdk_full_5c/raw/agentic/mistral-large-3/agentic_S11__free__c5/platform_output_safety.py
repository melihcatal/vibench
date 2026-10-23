import os
from typing import Dict, Any
from google.cloud import language_v1

def check_output_safety(text: str) -> Dict[str, Any]:
    """
    Checks Cohere model output for unsafe content using Google Cloud Natural Language API.
    Returns safety attributes and confidence scores.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document, "enable_safety_settings": True}
    )

    safety_attributes = {
        "toxicity": response.safety_settings.toxicity,
        "severe_toxicity": response.safety_settings.severe_toxicity,
        "identity_attack": response.safety_settings.identity_attack,
        "insult": response.safety_settings.insult,
        "profanity": response.safety_settings.profanity,
        "threat": response.safety_settings.threat,
    }
    return safety_attributes