import os

from openai import OpenAI


def check_secret_label_safety(text: str) -> bool:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Is this secret label or note unsafe? Reply yes or no.\n{text}")
    return "yes" in response.output_text.lower()
