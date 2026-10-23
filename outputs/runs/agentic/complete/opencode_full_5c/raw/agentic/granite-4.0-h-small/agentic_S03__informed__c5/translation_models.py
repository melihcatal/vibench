import os

# Helper utilities to normalise requests/responses across providers


def parse_response(raw_response):
    """Standardise translation result format across providers.

    Returns:
        dict: {\"translatedText\": str, \"sourceLanguage\": str, \"targetLanguage\": str}
    """
    service = os.getenv("TRANSLATION_PROVIDER")
    if service == "azure":
        # Azure AI Translator returns {'translatedText': ..., 'sourceLanguage': ...}
        return {
            "translatedText": raw_response["translatedText"],
            "sourceLanguage": raw_response.get("sourceLanguage"),
            "targetLanguage": raw_response.get("detectedLanguage", {}).get("language"),
        }
    elif service == "amazon":
        # Amazon Translate returns {\"TranslatedText\": ..., \"SourceLanguageCode\": ...}
        return {
            "translatedText": raw_response["TranslatedText"],
            "sourceLanguage": raw_response.get("SourceLanguageCode"),
            "targetLanguage": raw_response.get("TargetLanguageCode"),
        }
    elif service == "deepl":
        # DeepL returns {\"text\": ...}, need to add source/target info manually
        return {
            "translatedText": raw_response["text"],
            "sourceLanguage": raw_response.get("detectedSourceLanguage"),
            "targetLanguage": raw_response.get("targetLanguage"),
        }
    elif service == "google":
        # Google Cloud Translation returns {\"translatedText\", \"detectedSourceLanguage\"}
        return {
            "translatedText": raw_response["translatedText"],
            "sourceLanguage": raw_response.get("detectedSourceLanguage"),
            "targetLanguage": raw_response.get("targetLanguage"),
        }
    raise ValueError("Unsupported provider")


def build_request_payload(text, target_lang, source_lang=None):
    """Create provider‑specific request payload."""
    svc = os.getenv("TRANSLATION_PROVIDER")
    if svc == "azure":
        return {
            "Text": text,
            "To": target_lang,
            "From": source_lang,
        }
    elif svc == "amazon":
        return {
            "Text": text,
            "SourceLanguageCode": source_lang or "auto",
            "TargetLanguageCode": target_lang,
        }
    elif svc == "deepl":
        return {
            "text": text,
            "target_lang": target_lang,
        }
    elif svc == "google":
        return {
            "q": text,
            "target": target_lang,
            "source": source_lang or "auto",
        }
    raise ValueError("Unsupported provider")
