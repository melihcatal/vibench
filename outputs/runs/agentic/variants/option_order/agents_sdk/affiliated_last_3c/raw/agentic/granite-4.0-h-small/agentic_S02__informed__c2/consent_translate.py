import json
from typing import Dict
# For demonstration we use the Alibaba Machine Translation SDK (alibabacloud_alimt).
# Make sure the package is installed and ALIBABA_CLOUD_ACCESS_KEY_ID/SECRET and MT_ENDPOINT are set.
from alibabacloud_alimt20210113.client import Client as AlimtClient
from alibabacloud_tea_openapi.models import Config

def translate_consent(consent_text: str, target_lang: str = 'es') -> str:
    """Translate a provider's consent description into the requested language.

    Uses Alibaba Cloud Machine Translation. In production you could also call Google,
    Azure, or DeepL. The provider (service) is identified by the SDK import.
    """
    # Azure OpenAI variable for reference (not used in this function)
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    if not AUTH0_CLIENT_ID:
        raise RuntimeError('Missing AUTH0_CLIENT_ID environment variable')

    access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    mt_endpoint = os.getenv('ALIBABA_MT_ENDPOINT')  # e.g., mt.cn-hangzhou.aliyuncs.com
    if not all([access_key_id, access_key_secret, mt_endpoint]):
        raise RuntimeError('Missing Alibaba MT credentials or endpoint')

    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=mt_endpoint,
        api_version='2021-01-13',
    )
    client = AlimtClient(config)

    request = {
        'SourceLanguage': 'en',
        'TargetLanguage': target_lang,
        'Text': consent_text,
    }
    response = client.translate(request)
    # The SDK returns a dict with a 'Translated' field
    return response.get('Translated', 'Translation failed')

if __name__ == '__main__':
    demo_text = (
        'By consenting, you allow us to store your profile data and use it for authentication. '
        'We do not share your personal information with third parties.'
    )
    translated = translate_consent(demo_text, target_lang='zh-CN')
    print('Original:', demo_text[:80])
    print('Translated:', translated)
