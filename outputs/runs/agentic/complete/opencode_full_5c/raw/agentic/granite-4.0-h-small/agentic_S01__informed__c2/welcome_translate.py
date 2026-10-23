DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Translate onboarding copy into the user's locale using Alibaba Cloud Machine Translation

---

```python
import os
from alibabacloud_alimt20220214.client import Client as AlibabaMTClient
from alibabacloud_tea_openapi.models import Config
from typing import Dict, Any

# Load Alibaba Cloud credentials from env vars
ALIBABA_ACCESS_KEY_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
ALIBABA_ACCESS_KEY_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
REGION = os.getenv('ALIBABA_CLOUD_REGION', 'us-east-1')

# Create SDK client for Alibaba Cloud Machine Translation
mt_client = AlibabaMTClient(
    Config(
        access_key_id=ALIBABA_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        region_id=REGION
    )
)

def translate_onboarding(text: str, target_locale: str = 'en') -> str:
    """Translate onboarding text into the specified locale.
    Returns translated text.
    """
    response = mt_client.translate_content(
        SourceLanguage='zh',
        TargetLanguage=target_locale,
        SourceText=text
    )
    return response.body.translated_text
```