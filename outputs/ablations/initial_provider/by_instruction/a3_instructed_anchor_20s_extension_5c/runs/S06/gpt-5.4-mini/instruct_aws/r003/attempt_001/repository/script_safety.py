import os

from openai import OpenAI


def check_script_safety(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Classify this narration script for unsafe content and return JSON with safe and reasons: {text}",
    )
    return {"result": response.output_text}
