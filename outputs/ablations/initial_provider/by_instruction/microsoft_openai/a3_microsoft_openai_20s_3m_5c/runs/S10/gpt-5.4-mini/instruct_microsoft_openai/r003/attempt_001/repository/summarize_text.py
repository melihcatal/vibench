from model_client import load_config, make_client, system_user_messages


def summarize_text(text: str) -> str:
    config = load_config("summarize")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=system_user_messages("You summarize long text concisely.", text),
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
