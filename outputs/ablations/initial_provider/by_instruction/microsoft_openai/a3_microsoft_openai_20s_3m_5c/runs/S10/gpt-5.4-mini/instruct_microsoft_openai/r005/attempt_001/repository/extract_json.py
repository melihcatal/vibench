from model_client import get_client, get_model


def extract_json(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Extract structured JSON from the input text."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or "{}"
