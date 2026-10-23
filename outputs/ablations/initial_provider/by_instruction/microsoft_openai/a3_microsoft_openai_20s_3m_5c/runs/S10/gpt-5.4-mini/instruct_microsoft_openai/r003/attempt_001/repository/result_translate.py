from model_client import load_config, make_client


def result_translate(text: str, target_language: str) -> str:
    config = load_config("translate")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": f"Translate the text into {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
