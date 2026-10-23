import os, json, requests

def check_log_safety(message_text, safe_threshold=0.5):
    """Check a log message for unsafe content using Perspective API (free tier).

    Returns True if safe, False otherwise.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set')
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": message_text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    # Toxicity score between 0 and 1
    toxicity = result.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value', 0.0)
    is_safe = toxicity < safe_threshold
    return is_safe

# Helper for batch checking
def filter_safe_logs(log_events, safe_threshold=0.5):
    safe_logs = []
    for ev in log_events:
        msg = json.loads(ev['message']) if isinstance(ev['message'], str) else ev['message']
        text = msg.get('text') or msg.get('msg')
        if text and check_log_safety(text, safe_threshold):
            safe_logs.append(ev)
    return safe_logs
