import os
from google.cloud import translate_v2 as translate

# Local helpers
from translation_client import get_translation_client
from translation_models import validate_language_code

def summarize_quality(translated_text: str, source_lang: str, target_lang: str) -> dict:
    """Analyzes a translated string for common quality issues using Google Translate API's detection.

    Returns a dictionary with issue counts/metrics.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    # Use Cloud Translation's detectLanguage on both source and target to check for unexpected shifts
    source_detection = client.detect_language(source_lang)['language']
    target_detection = client.detect_language(translated_text)['language']
    result = {
        'original_target_lang': target_lang,
        'detected_source': source_detection,
        'detected_target': target_detection,
        'language_shift': source_detection != target_lang,
        # Simple heuristic: length reduction >50% may indicate lossy translation
        'potential_lossy': len(translated_text) < 0.5 * len(source_lang)
    }
    return result

if __name__ == "__main__":
    sample = "Hello"
    print(summarize_quality(sample, 'en', 'es'))