from model_client import build_client, load_config


def summarize_text(text: str, provider: str = "openai") -> str:
    config = load_config(provider=provider)
    client = build_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Summarize long text concisely."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
