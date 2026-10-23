from database_client import get_comprehend_client

def record_summary(text: str, language_code: str = "en") -> list[str]:
    """
    Summarizes a given text using AWS Comprehend's key phrase detection.
    Returns a list of key phrases.
    """
    comprehend = get_comprehend_client()

    response = comprehend.detect_key_phrases(
        Text=text,
        LanguageCode=language_code
    )

    key_phrases = [phrase["Text"] for phrase in response.get("KeyPhrases", [])]
    return key_phrases
