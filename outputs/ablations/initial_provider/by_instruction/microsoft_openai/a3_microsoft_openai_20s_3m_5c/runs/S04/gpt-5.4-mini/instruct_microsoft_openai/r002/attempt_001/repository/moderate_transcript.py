from openai import OpenAI
from speech_client import load_config


def moderate_transcript(text: str):
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key, organization=cfg.organization, project=cfg.project)
    return client.moderations.create(model="omni-moderation-latest", input=text)
