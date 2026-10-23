import os
from storage_client import get_comprehend_client


def summarize_asset_content(payload, config=None):
    config = config or {}
    text_to_summarize = payload["text"]
    language_code = payload.get("language_code", "en")  # Default to English

    comprehend_client = get_comprehend_client(config.get("region"))

    # Comprehend's `detect_key_phrases` or `detect_entities` can be used as a proxy for summarization
    # For a true summarization, often a more advanced NLP model or service would be used.
    # Here, we'll extract key phrases as a form of content summarization.
    try:
        response = comprehend_client.detect_key_phrases(
            Text=text_to_summarize,
            LanguageCode=language_code
        )
        key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
        return {"key_phrases": key_phrases}
    except Exception as e:
        raise RuntimeError(f"Error summarizing asset content with Comprehend: {e}")
