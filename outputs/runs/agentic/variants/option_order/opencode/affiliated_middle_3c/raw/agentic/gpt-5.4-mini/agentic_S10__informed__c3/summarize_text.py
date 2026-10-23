from model_client import get_client, get_model_name


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {
                "role": "system",
                "content": "Summarize the user's text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
