import os, json, requests
from observability_models import SimpleLogMsg
from typing import List

# Provider: watsonx.ai guardrails / HAP detection (REST)
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
BASE_URL = f'https://{WATSONX_PROJECT_ID}.watsonx.ibm.com/guardrails/v1/moderation'

def is_safe(text: str) -> bool:
    """Check a single log message for unsafe content using watsonx guardrails."""
    payload = {
        'input': text,
        'attributes': ['hate', 'harassment', 'self_harm']
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {WATSONX_API_KEY}'
    }
    r = requests.post(BASE_URL, headers=headers, json=payload, timeout=5)
    r.raise_for_status()
    result = r.json()
    # The response includes a 'moderation' field; count violations
    violations = result.get('moderation', {}).get('results', [])
    return len(violations) == 0

def filter_safe(logs: List[SimpleLogMsg]) -> List[SimpleLogMsg]:
    """Return only the log entries whose text passes safety checking."""
    safe_logs = []
    for log in logs:
        if is_safe(log['message']):
            safe_logs.append(log)
    return safe_logs

if __name__ == '__main__':
    sample = [
        {'message': 'User reported a bug', 'timestamp': '2025-08-15T12:00:00Z', 'level': 'INFO', 'correlation_id': 'c1'},
        {'message': 'Attackers hacked', 'timestamp': '2025-08-15T12:01:00Z', 'level': 'WARNING', 'correlation_id': 'c2'}
    ]
    safe = filter_safe(sample)
    print(json.dumps(safe, indent=2))
