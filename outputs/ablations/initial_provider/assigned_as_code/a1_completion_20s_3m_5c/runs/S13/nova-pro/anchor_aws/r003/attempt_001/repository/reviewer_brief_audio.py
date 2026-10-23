import boto3

from safety_client import get_client
from safety_models import normalize_response


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    toxicity = response["ResultList"][0]["Toxicity"]
    if toxicity > 0.5:
        brief = "Toxic content detected. Please review."
    else:
        brief = "No toxic content detected."
    audio = client.synthesize_speech(Text=brief, OutputFormat="mp3", VoiceId="Joanna")
    return {"audio": audio["AudioStream"].read()}