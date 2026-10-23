import re
from typing import List, Tuple
from safety_models import UnsafeSpan
from safety_client import SizeLimitedJSONEncoder

# Dummy provider: openai moderation endpoint for span detection
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = 'https://api.openai.com/v1/moderations'

_introspection_severity_threshold = 0.5

def redact_unsafe(text: str, context_size: int = 10) -> Tuple[str, List[UnsafeSpan]]:
    """Flags or redacts unsafe spans from text using OpenAI Moderation API.

    Returns the (potentially redacted) text and a list of detected unsafe spans.
    """
    payload = {
        "input": text,
        "model": "moderation"
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    flags = response.json()['flags']
    unsafe_spans: List[UnsafeSpan] = []
    for flag, info in flags.items():
        # Only consider flagged categories with sufficient severity
        if info.get('category') == 'Hate' and info['severity'] >= _introspection_severity_threshold:
            # Simple heuristic to locate the span; try to find the flag word in text
            words = info['detail'].split()
            for word in words:
                match = re.search(re.escape(word), text, re.IGNORECASE)
                if match:
                    start, end = match.span()
                    unsafe_spans.append(UnsafeSpan(start=start, end=end, category='Hate'))
    # Redact detected spans with asterisks
    redacted = text
    # Sort spans by start descending to avoid shifting indices
    for span in sorted(unsafe_spans, key=lambda s: s.start, reverse=True):
        redacted = redacted[:span.start] + '*' * (span.end - span.start) + redacted[span.end:]
    return redacted, unsafe_spans
