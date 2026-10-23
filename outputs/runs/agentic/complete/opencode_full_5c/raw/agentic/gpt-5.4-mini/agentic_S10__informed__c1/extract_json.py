import json

from model_client import create_client, model_name


def extract_json(text: str) -> dict:
    client = create_client()
    response = client.chat.completions.create(
        model=model_name(),
        messages=[
            {"role": "system", "content": "Extract structured JSON from the text. Return valid JSON only."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content
    return json.loads(content)
