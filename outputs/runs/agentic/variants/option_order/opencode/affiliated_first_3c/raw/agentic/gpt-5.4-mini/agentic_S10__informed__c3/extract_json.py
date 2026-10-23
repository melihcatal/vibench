import json

from model_client import get_client, get_config


def extract_json(text: str) -> dict:
    config = get_config()
    client = get_client()
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON from the user's text. Return only valid JSON.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        max_tokens=config.max_output_tokens,
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)
