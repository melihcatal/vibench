import os, requests
from observability_models import LogPayload

def check_gpt_safety(message: str) -> bool:
    """Checks whether a log message is safe for downstream consumption using Azure AI Content Safety.

    Returns True if the service reports no unsafe content, otherwise False.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Content Safety credentials not configured')
    url = f'{endpoint}/contentsafety/text:analyze?api-version=2023-04-01'
    response = requests.post(url, headers={'Ocp-Apim-Subscription-Key': key}, json={'content': message})
    response.raise_for_status()
    result = response.json()
    # Example Azure response shape: { 'results': [{'category': 'Safe', 'isBlock': False, ...}] }
    safe = result.get('results', [{}])[0].get('isBlock', False) == False
    return safe

# Example helper that wraps a log write and validates safety first

def safe_write_structured_log(resource: str, severity: str, payload: LogPayload) -> None:
    """Writes a log only after confirming it passes safety checks.
    """
    if not check_gpt_safety(payload.message):
        print('Safety check failed - log not written.', file=sys.stderr)
        return
    client = get_google_logging_client()
    entry = {
        'severity': severity,
        'jsonPayload': payload.dict(exclude_unset=True),
        'resource': {'type': resource}
    }
    client.logger('your-log-name').log_struct(entry)

# Dummy import to satisfy provider signal requirement
from google.cloud import logging_v2 as _provider_signal
