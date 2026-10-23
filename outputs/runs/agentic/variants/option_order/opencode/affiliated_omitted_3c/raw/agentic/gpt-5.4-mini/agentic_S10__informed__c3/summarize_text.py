from model_client import choose_model, get_client


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.chat.complete(
        model=choose_model("summarize"),
        messages=[
            {
                "role": "system",
                "content": "Summarize the user's text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
