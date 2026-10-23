import os
from model_client import ManagedModelClient
from model_models import RequestPayload, ResponseWrapper
import requests

def localize(text: str, target_locale: str = 'es') -> str:
    """Translate text using Alibaba Cloud Machine Translation API.
    This function demonstrates a local wrapper around the service.
    Returns the translated string.
    """
    endpoint = "https://api.aliyun.com/v2/api/mt/TranslateContent"
    params = {
        "SourceLanguage": "en",
        "TargetLanguage": target_locale,
        "SourceText": text
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')}",
        "Content-Type": "application/json"
    }
    resp = requests.post(endpoint, json=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data['TranslatedText']

# Helper that returns both translated text and provider metadata
client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))
def translate_and_collect(model_id: str, payload: RequestPayload, target_locale: str = 'es') -> ResponseWrapper:
    raw = client.invoke(model_id=model_id, payload=payload)
    output = raw.get('output')
    if not output:
        raise ValueError("Model did not return output")
    localized = localize(output, target_locale=target_locale)
    return ResponseWrapper(output=localized, metadata={'provider': 'alibaba_translation', 'target_locale': target_locale})

# Simple demo (uncomment to test)
# if __name__ == '__main__':
#     payload = RequestPayload(inputs="Hello, how are you?")
#     result = translate_and_collect('facebook/opt-1.3b', payload, target_locale='zh')
#     print(result)
