import anthropic
import os


def extract_json(text: str) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        temperature=0.0,
        messages=[{"role": "user", "content": text}],
        system="You are a helpful assistant. Extract structured JSON from the provided text. Return only valid JSON.",
    )
    return response.content[0].text
