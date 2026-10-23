import json

from model_client import choose_model, get_client


def extract_json(text: str) -> dict:
    client = get_client()
    response = client.chat.complete(
        model=choose_model("extract_json"),
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON from the user's text. Return only valid JSON.",
            },
            {"role": "user", "content": text},
        ],
    )
    content = response.choices[0].message.content
    return json.loads(content)
