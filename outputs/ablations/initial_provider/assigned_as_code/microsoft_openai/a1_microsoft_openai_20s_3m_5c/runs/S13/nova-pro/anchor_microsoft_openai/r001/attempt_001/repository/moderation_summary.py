from.safety_client import get_client
from.safety_models import parse_response


def moderation_summary(payloads, config=None):
    client = get_client(config)
    results = []
    for payload in payloads:
        response = client.analyze_text(payload)
        results.append(parse_response(response))
    return {'summary': results}