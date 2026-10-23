import os

from openai import OpenAI


def main(text: str = "") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize the incident from these logs:\n{text}")
    return response.output_text
