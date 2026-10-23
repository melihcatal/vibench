import boto3

from safety_client import get_client
from safety_models import normalize_response


def safety_threshold(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    toxicity = response["ResultList"][0]["Toxicity"]
    if toxicity > config.get("threshold", 0.5):
        return {"allow": False}
    else:
        return {"allow": True}