import json

from model_client import load_config, make_client, system_user_messages


def extract_json(text: str) -> dict:
    config = load_config("extract")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=system_user_messages("Return only valid JSON extracted from the input.", text),
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)
