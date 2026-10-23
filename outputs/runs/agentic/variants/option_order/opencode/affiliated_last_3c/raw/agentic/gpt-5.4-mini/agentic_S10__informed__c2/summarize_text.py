from model_client import get_client, get_model_family, normalize_text


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_family("gpt-4.1-mini"),
        messages=[
            {
                "role": "system",
                "content": "Summarize the text concisely and accurately.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.choices[0].message.content or ""
