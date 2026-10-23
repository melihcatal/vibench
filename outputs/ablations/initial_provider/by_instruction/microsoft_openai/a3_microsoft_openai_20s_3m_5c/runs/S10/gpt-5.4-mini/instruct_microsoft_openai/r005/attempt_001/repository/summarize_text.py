from model_client import get_client, get_model


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "Summarize long text concisely."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
