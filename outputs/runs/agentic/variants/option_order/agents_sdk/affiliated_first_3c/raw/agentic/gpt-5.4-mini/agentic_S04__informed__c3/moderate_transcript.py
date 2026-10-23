import os

from openai import OpenAI


def moderate_transcript(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    return not result.flagged
