import json

from model_client import get_client, pick_model


def extract_json(text: str) -> dict:
    client = get_client()
    model = pick_model("extract_json")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON from the user's text. Return only valid JSON.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content or "{}")
