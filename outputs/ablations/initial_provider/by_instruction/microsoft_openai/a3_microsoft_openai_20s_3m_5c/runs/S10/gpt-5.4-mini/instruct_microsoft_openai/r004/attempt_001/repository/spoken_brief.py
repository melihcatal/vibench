from model_client import build_client, load_config


def spoken_brief(text: str, provider: str = "openai") -> str:
    config = load_config(provider=provider)
    client = build_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Rewrite the text as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
