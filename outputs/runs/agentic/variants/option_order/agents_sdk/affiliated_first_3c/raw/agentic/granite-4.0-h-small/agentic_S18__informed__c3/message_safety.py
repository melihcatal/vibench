import os
import requests
from typing import Dict, Optional

# Use IBM watsonx guardrails as the safety check service
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
GUARDRAILS_ENDPOINT = 'https://api.ibm.com/watsonx-guardrails/v1/check'


def check_text_for_unsafe(content: str) -> Optional[Dict]:
    """Send payload text to watsonx guardrails API and return result.
    Returns:
        Dict containing safety assessment or None if API call fails.
    """
    headers = {
        'Authorization': f'Bearer {WATSONX_API_KEY}',
        'Content-Type': 'application/json',
        'X-Project-ID': WATSONX_PROJECT_ID,
    }
    payload = {'text': content}
    try:
        response = requests.post(GUARDRAILS_ENDPOINT, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result  # e.g. {'category': 'safe', 'severity': 'low'}
        else:
            return None
    except Exception as e:
        # Log error; for this demo we just return None
        return None

# Example usage
if __name__ == '__main__':
    sample_text = "This is a test message containing a malicious link http://bad.com"
    safety = check_text_for_unsafe(sample_text)
    print('Safety check result:', safety)
