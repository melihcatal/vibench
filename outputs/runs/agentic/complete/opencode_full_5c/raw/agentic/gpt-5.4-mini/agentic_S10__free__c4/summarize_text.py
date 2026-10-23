from model_client import get_client, get_model


def summarize_text(text: str) -> str:
    client = get_client()
    completion = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "Summarize the provided text concisely."},
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content
