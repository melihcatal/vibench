from openai import OpenAI
import os

def profile_moderation(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    return not response.results[0].flagged
