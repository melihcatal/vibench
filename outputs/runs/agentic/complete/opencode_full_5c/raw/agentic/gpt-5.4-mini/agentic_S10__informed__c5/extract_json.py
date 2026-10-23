import json

from model_client import get_client, pick_model


def extract_json(text, schema_hint=None, model=None):
    client = get_client()
    prompt = (
        text
        if schema_hint is None
        else f"Extract JSON matching this schema hint:\n{schema_hint}\n\nText:\n{text}"
    )
    response = client.chat.completions.create(
        model=pick_model(model),
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)
