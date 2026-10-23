from model_client import load_config, make_client


def spoken_brief(text: str) -> str:
    config = load_config("spoken")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Rewrite the content as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
