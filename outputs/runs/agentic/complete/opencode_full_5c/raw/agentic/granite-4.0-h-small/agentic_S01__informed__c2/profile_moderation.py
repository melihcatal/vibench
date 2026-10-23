DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Moderate profile text before account activation using Alibaba Cloud Content Moderation (Green)

---

```python
import os
from alibabacloud_green20200514.client import Client as GreenClient
from alibabacloud_tea_openapi.models import Config
from typing import Dict, Any

# Load Alibaba Cloud credentials from env vars
ALIBABA_ACCESS_KEY_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
ALIBABA_ACCESS_KEY_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
REGION = os.getenv('ALIBABA_CLOUD_REGION', 'us-east-1')

# Configure Green SDK client
green_client = GreenClient(
    Config(
        access_key_id=ALIBABA_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        region_id=REGION
    )
)

def moderate_profile_text(text: str) -> Dict[str, Any]:
    """Run Alibaba Green content moderation on profile text.
    Returns moderation result with safe flag and any hit labels.
    """
    response = green_client.text_scan(
        Data='text',
        Scene=['antispam'],
        Content=text
    )
    # Simplified result handling - assume safe if no violations
    result = response.body.data[0] if response.body.data else {}
    safe = result.get('hitFlag', '0') == '0'
    labels = result.get('labels', [])
    return {'safe': safe, 'labels': labels}
```