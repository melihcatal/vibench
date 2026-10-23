import os, requests, json
from observability_models import LogPayload

def translate_to(target_locale: str, source_text: str) -> str:
    """Translates a log message to another locale using Azure AI Translator.

    Returns the translated string.
    """
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    key = os.getenv('AZURE_TRANSLATOR_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Translator credentials not configured')
    url = f'{endpoint}/translate?api-version=3.0&to={target_locale}'
    headers = {'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}
    body = [{'Text': source_text}]
    resp = requests.post(url, headers=headers, json=body)
    resp.raise_for_status()
    translations = resp.json()[0].get('translations', [])
    return translations[0]['text'] if translations else source_text

# Example wrapper that translates a log payload before writing

def translated_write_structured_log(resource: str, severity: str, original_payload: LogPayload) -> None:
    """Writes a log after translating its message field.
    """
    translated_msg = translate_to('es', original_payload.message)  # example Spanish translation
    enriched_payload = original_payload.copy(update={'message': translated_msg})
    client = get_google_logging_client()
    entry = {
        'severity': severity,
        'jsonPayload': enriched_payload.dict(exclude_unset=True),
        'resource': {'type': resource}
    }
    client.logger('your-log-name').log_struct(entry)

# Provider signal import for Azure Translator
from azure.ai.translation import TranslatorClient as _provider_signal
