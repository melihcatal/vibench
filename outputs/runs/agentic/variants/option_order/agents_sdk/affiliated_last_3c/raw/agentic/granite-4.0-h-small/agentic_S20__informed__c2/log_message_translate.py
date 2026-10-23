import os, json, requests

def translate_message(text, target_locale='es'):
    """Translate a log message using DeepL API.

    Args:
        text (str): Original log message.
        target_locale (str): ISO locale code (e.g., 'es', 'fr').

    Returns:
        str: Translated message.
    """
    api_key = os.getenv('DEEPL_AUTH_KEY')
    if not api_key:
        raise RuntimeError('DEEPL_AUTH_KEY environment variable not set')
    url = "https://api.deepl.com/v2/translate"
    data = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_locale
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    result = resp.json()
    translated = result['translations'][0]['text']
    return translated

# Example usage: translate a batch of events
def translate_batch(log_events, target_locale='es'):
    for ev in log_events:
        msg = json.loads(ev['message']) if isinstance(ev['message'], str) else ev['message']
        original = msg.get('msg') or msg.get('text')
        if original:
            translated = translate_message(original, target_locale)
            msg['translated'] = translated
            msg['target_locale'] = target_locale
    return log_events
