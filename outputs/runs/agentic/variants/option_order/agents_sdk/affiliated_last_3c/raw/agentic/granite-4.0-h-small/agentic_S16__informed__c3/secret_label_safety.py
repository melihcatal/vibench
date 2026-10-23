import os
import alibabacloud_green
from typing import Any, Dict
from security_client import SecretClient

def check_sensitive_content(secret_id: str) -> bool:
    """Check secret content for sensitive/unsafe material using Alibaba Cloud Content Moderation.

    Returns True if the content is deemed safe, False otherwise.
    """
    client = alibabacloud_green.AcsClient(
        os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    secret_value = client.get_secret_value(SecretId=secret_id)
    notes = secret_value.get('SecretString', '')
    if not notes:
        raise ValueError('Secret contains no notes')
    # Alibaba Content Moderation API expects a JSON payload with a 'content' field
    response = client.content_moderation(
        text=notes
    )
    # Simplified evaluation: if the API returns 'pass' we consider it safe
    return response.get('result', {}).get('label') == 'pass'
