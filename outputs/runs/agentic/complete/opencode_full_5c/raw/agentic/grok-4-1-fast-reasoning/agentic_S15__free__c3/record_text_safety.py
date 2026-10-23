import openai
import os


def check_text_safety(text: str) -> dict:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return response.results[0].model_dump()
