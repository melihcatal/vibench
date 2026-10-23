from model_client import load_config, make_client


def prompt_safety(text: str) -> str:
    config = load_config("safety")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Classify text safety and return SAFE or UNSAFE with a brief reason."},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()
