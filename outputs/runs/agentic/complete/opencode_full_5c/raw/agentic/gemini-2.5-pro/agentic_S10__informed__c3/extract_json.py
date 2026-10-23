import json
from model_client import get_openai_client
from model_models import Message


def extract_json(text_with_json: str) -> dict:
    client = get_openai_client()

    messages = [
        Message(
            role="system",
            content="You are an expert in extracting structured JSON from text. Respond with only the JSON object.",
        ),
        Message(
            role="user", content=f"Extract the JSON from this text: {text_with_json}"
        ),
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[msg.dict() for msg in messages],
        response_format={"type": "json_object"},
    )

    if response.choices:
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {}
    return {}
