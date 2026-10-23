"""
payload_safety.py - Check decrypted text payloads for unsafe content using Amazon Comprehend.
"""
from security_client import get_comprehend_client

def check_payload_safety(text_payload: str, language_code: str = 'en') -> dict:
    """
    Analyzes a text payload for safety/toxicity using Amazon Comprehend.

    Args:
        text_payload: The decrypted text content to check.
        language_code: The language of the text (e.g., 'en' for English).

    Returns:
        A dictionary containing the sentiment and optionally, toxicity detection results.
        Note: Comprehend directly provides sentiment, PII, etc. For explicit 'toxicity',
        one might use a custom classifier or combine sentiment with other entities.
        Here, we'll use `detect_sentiment` and `detect_toxic_content` (if available/applicable
        or fall back to sentiment/key phrases if not directly a toxicity API).
        As per current boto3 comprehend, `detect_toxic_content` is available.
    """
    comprehend_client = get_comprehend_client()
    results = {}
    try:
        # Detect overall sentiment
        sentiment_response = comprehend_client.detect_sentiment(
            Text=text_payload,
            LanguageCode=language_code
        )
        results['Sentiment'] = sentiment_response

        # Detect toxic content (if available in the region/version)
        # Note: Availability of detect_toxic_content can vary by region and service updates.
        try:
            toxic_content_response = comprehend_client.detect_toxic_content(
                Text=text_payload,
                LanguageCode=language_code
            )
            results['ToxicContent'] = toxic_content_response
        except comprehend_client.exceptions.UnsupportedLanguageException:
            print(f"Toxic content detection not supported for language: {language_code}")
        except Exception as e:
            print(f"Could not perform toxic content detection: {e}")

    except Exception as e:
        print(f"Error checking payload safety with Amazon Comprehend: {e}")
        raise

    return results
