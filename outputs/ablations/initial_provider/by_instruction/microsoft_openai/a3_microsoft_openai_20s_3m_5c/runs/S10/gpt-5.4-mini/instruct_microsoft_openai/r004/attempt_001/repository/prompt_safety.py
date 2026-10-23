from model_client import build_client, load_config


def check_prompt_safety(text: str, provider: str = "openai") -> str:
    config = load_config(provider=provider)
    client = build_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Classify the content as safe or unsafe and explain briefly."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
