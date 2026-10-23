from model_client import get_openai_client, choose_chat_model


def summarize_text(text: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=choose_chat_model(model),
        messages=[
            {"role": "system", "content": "Summarize the provided text concisely."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
