# localized_platform_output.py
# [LATER-STEP] Translate platform model output for another locale

from google.cloud import translate_v2 as translate
import os

TRANSLATE_CLIENT = None

# Detect and initialize Google Cloud Translate client from env vars
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def _ensure_translate_client():
    global TRANSLATE_CLIENT
    if TRANSLATE_CLIENT is None:
        if CREDENTIALS_PATH:
            TRANSLATE_CLIENT = translate.Client.from_service_account_json(CREDENTIALS_PATH)
        else:
            # Default client using GOOGLE_APPLICATION_CREDENTIALS env
            TRANSLATE_CLIENT = translate.Client()


def localize_output(provider_response: dict, target_lang: str = 'es') -> dict:
    """Translate all textual content in a provider model response to the target locale.

    Args:
        provider_response: raw dict returned from the model platform.
        target_lang: ISO 639-1 code of the target language (default: 'es' for Spanish).

    Returns a dict with a new 'localized' key containing the translated text.
    """
    _ensure_translate_client()
    # Gather all text fragments from provider's choices (or any nested field)
    fragments = []
    for choice in provider_response.get('choices', []):
        # naive extraction; adapt to provider's actual field names
        delta = choice.get('delta', {})
        fragments.append(delta.get('content', ''))
    raw_text = ' '.join(fragments)
    if not raw_text:
        return {'output': provider_response, 'localized': None}
    # Call Google Translate API
    result = TRANSLATE_CLIENT.translate(raw_text, target_language=target_lang)
    localized_text = result.get('translatedText', '')
    # Re‑assemble a response that mimics the original shape but with localized text
    localized_response = provider_response.copy()
    localized_response['localized'] = {
        'choices': [
            {
                'delta': {
                    'content': localized_text
                }
            }
        ]
    }
    return {'output': provider_response, 'localized': localized_response}

if __name__ == "__main__":
    # Demo: translate a dummy response to French
    dummy = {
        "choices": [
            {"delta": {"content": "Hello world"}}
        ]
    }
    print(localize_output(dummy, target_lang='fr'))
