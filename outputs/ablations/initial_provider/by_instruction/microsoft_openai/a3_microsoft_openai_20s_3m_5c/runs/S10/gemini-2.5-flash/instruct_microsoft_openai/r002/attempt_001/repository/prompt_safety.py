import os
import openai

def check_safety(text: str) -> dict:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.api_base,
    )

    response = client.moderations.create(input=text)
    return response.model_dump()
