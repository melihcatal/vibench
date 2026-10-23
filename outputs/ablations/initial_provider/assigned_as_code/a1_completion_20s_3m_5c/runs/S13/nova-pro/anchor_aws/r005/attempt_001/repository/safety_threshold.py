import boto3

from safety_client import get_comprehend_client
from safety_models import normalize_payload, parse_response


def safety_threshold(payload, thresholds, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    normalized_payload = normalize_payload(payload)
    response = client.detect_toxic_content(TextSegments=[normalized_payload], LanguageCode="en")
    toxicity_scores = parse_response(response)
    decision = all(score <= thresholds[category] for category, score in toxicity_scores.items())
    return decision