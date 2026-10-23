import os
from typing import Optional, Dict, Any
from google.cloud import language_v1
from model_client import get_llm_client


def check_prompt_safety(text: str, language: str = "en") -> Dict[str, Any]:
    """
    Checks if the provided text contains unsafe content using Google Cloud Natural Language API.

    Args:
        text: The input text to check for safety.
        language: The language of the input text.

    Returns:
        A dictionary containing safety analysis results.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=language
    )

    response = client.analyze_sentiment(request={"document": document})

    # Additional safety checks can be added here
    return {
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "is_safe": response.document_sentiment.score >= -0.5,
    }
