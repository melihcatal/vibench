from model_client import get_client, get_config


def summarize_text(text: str) -> str:
    config = get_config()
    client = get_client()
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Summarize the user's text concisely."},
            {"role": "user", "content": text},
        ],
        temperature=config.temperature,
        max_tokens=config.max_output_tokens,
    )
    return response.choices[0].message.content or ""
