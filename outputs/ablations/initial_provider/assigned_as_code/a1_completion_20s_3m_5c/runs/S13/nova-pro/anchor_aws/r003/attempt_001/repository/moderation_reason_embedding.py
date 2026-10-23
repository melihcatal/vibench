import boto3

from safety_client import get_client
from safety_models import normalize_response


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    toxicity = response["ResultList"][0]["Toxicity"]
    if toxicity > 0.5:
        reason = "Toxic content detected"
    else:
        reason = "No toxic content detected"
    embedding = client.embed_text(Text=reason, LanguageCode="en")
    return {"embedding": embedding["Embedding"]}