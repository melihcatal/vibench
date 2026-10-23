import os
from openai import OpenAI


def key_usage_summary(text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize key usage and crypto events: {text}"
    )
    return response.output_text


if __name__ == "__main__":
    key_usage_summary(os.environ.get("TEXT", ""))
