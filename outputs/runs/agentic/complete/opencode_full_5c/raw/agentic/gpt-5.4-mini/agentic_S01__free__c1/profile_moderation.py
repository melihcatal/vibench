import os

from openai import OpenAI


def profile_moderation(profile_text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    resp = client.moderations.create(
        model="omni-moderation-latest",
        input=profile_text,
    )
    return resp.results[0].model_dump() if resp.results else {}
