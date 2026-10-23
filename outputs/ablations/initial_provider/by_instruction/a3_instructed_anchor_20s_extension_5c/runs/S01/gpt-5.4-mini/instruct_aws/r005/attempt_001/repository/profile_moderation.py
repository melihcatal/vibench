from openai import OpenAI

from identity_client import openai_api_key
from identity_models import ModerationRequest


def profile_moderation(text: str):
    req = ModerationRequest(text=text)
    client = OpenAI(api_key=openai_api_key())
    return client.moderations.create(input=req.text, model="omni-moderation-latest")
