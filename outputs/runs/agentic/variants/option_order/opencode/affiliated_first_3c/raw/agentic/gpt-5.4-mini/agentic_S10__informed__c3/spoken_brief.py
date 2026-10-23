from model_client import get_client, get_config


def spoken_brief(text: str) -> str:
    config = get_config(model="gpt-4.1-mini")
    client = get_client()
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Rewrite the text as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
        max_tokens=256,
    )
    return response.choices[0].message.content or ""
