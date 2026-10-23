from model_client import create_client, load_settings


def spoken_brief(text: str) -> str:
    settings = load_settings()
    client = create_client()
    response = client.messages.create(
        model=settings.model,
        max_tokens=256,
        temperature=0.3,
        system="Rewrite the content as a short spoken brief.",
        messages=[{"role": "user", "content": text}],
    )
    return "".join(block.text for block in response.content if hasattr(block, "text"))
