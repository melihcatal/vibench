from database_client import get_comprehend_client
from typing import Dict, Any, List


def summarize_record(text_content: str) -> Dict[str, Any]:
    """
    Summarizes text content from a document record using AWS Comprehend to extract key phrases.

    Args:
        text_content: The text field of a document record to summarize.

    Returns:
        A dictionary containing the detected language and a list of key phrases.
    """
    comprehend = get_comprehend_client()

    summary_results = {"detected_language": "unknown", "key_phrases": []}

    if not text_content or not isinstance(text_content, str):
        return summary_results

    # Detect dominant language first
    try:
        language_response = comprehend.detect_dominant_language(Text=text_content)
        if language_response and language_response["Languages"]:
            dominant_language = language_response["Languages"][0]["LanguageCode"]
            summary_results["detected_language"] = dominant_language

            # Extract key phrases in the detected language
            key_phrases_response = comprehend.detect_key_phrases(
                Text=text_content, LanguageCode=dominant_language
            )
            if key_phrases_response and key_phrases_response["KeyPhrases"]:
                summary_results["key_phrases"] = [
                    phrase["Text"] for phrase in key_phrases_response["KeyPhrases"]
                ]

    except Exception as e:
        print(f"Error summarizing text with AWS Comprehend: {e}")

    return summary_results
