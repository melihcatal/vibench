import os
import requests
from safety_models import ModerationRequest

def translate_appeal(appeal_text: str, target_lang: str = 'es') -> str:
    """Translate appeal (review) text using Alibaba Cloud Machine Translation.
    Returns the translated string.
    """
    # Alibaba Cloud Translation endpoint (REST)
    endpoint = os.getenv('ALIBABA_TRANSLATE_ENDPOINT', 'https://mt.cn-hangzhou.aliyuncs.com')
    access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    if not all([endpoint, access_key_id, access_key_secret]):
        raise RuntimeError('Alibaba Translate credentials not configured')
    # Prepare request payload
    payload = {
        'SourceLanguage': 'en',
        'TargetLanguage': target_lang,
        'Text': appeal_text,
    }
    headers = {
        'Content-Type': 'application/json',
        'Date': format(requests.utils.format_datetime(requests.utils.utcnow()), '%a, %d %b %Y %H:%M:%S GMT'),
        'Authorization': _generate_alibaba_signature(endpoint, payload, access_key_id, access_key_secret),
    }
    resp = requests.post(endpoint + '/api/x-acs-translate', json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    return result.get('Translated')

def _generate_alibaba_signature(url: str, payload: dict, ak: str, sk: str) -> str:
    # Minimal v3 signature generation (not production ready)
    import hmac, hashlib, base64
    string_to_sign = f'{url}\n{payload}'
    hmac_digest = hmac.new(sk.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    return 'acs ' + ak + ':' + base64.b64encode(hmac_digest).decode()

# Example usage
if __name__ == '__main__':
    sample = 'I disagree with the decision.'
    print(translate_appeal(sample))
