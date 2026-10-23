import os

from openai import OpenAI


def check_live_caption_safety(text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Classify this live transcript as safe or unsafe and explain briefly: {text}",
    )
    return response.output_text
