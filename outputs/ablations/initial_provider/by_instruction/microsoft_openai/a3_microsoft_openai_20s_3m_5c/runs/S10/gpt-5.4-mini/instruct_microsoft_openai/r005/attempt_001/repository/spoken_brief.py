from model_client import get_client, get_model


def spoken_brief(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "Rewrite the text as a brief spoken summary."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
