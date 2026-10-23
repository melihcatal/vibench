import os
from typing import List
from observability_models import LogEvent
from observability_client import get_datadog_client

def check_text_safety(text: str) -> bool:
    """Validate a log message string for unsafe or disallowed content using Tisane API.

    Returns True if the text passes moderation, False otherwise.
    """
    tisane_key = os.getenv('TISANE_API_KEY')
    if not tisane_key:
        raise RuntimeError('Missing TISANE_API_KEY environment variable')
    import requests
    url = 'https://api-portal.tisane.ai/v2/text'
    payload = {'text': text}
    headers = {'Authorization': f'Bearer {tisane_key}', 'Content-Type': 'application/json'}
    resp = requests.post(url, json=payload, headers=headers, timeout=5)
    data = resp.json()
    is_safe = data.get('moderation', {}).get('is_safe', False)
    return is_safe


def safe_log_payload(event: LogEvent) -> LogEvent:
    """If the event message fails safety check, raise an exception.
    """
    if not check_text_safety(event.message):
        raise ValueError('Log message contains unsafe content and cannot be ingested.')
    return event
