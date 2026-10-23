import json
from safety_client import SafetyClient
from safety_models import ModerationRequest, Flag, Category

def moderation_summary(text: str) -> dict:
    """Generate a concise moderation summary for a single text using Azure AI Content Safety.
    Returns a JSON‑serializable dict.
    """
    client = SafetyClient()
    request = ModerationRequest(text=text)
    response = client.check_content(request)

    summary = {
        'text': text,
        'unsafe': any(f.severity >= f.WARNING for f in response.flags),
        'flags': [
            {
                'category': f.category,
                'severity': f.severity.name,
                'span': (f.start_char, f.end_char)
            }
            for f in response.flags
        ]
    }
    return summary

# Example CLI usage (optional)
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python moderation_summary.py <text>')
        sys.exit(1)
    txt = ' '.join(sys.argv[1:])
    print(json.dumps(moderation_summary(txt), indent=2))
