from model_client import create_client, load_settings


def summarize_text(text: str) -> str:
    settings = load_settings()
    client = create_client()
    response = client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        system="Summarize the given text concisely and accurately.",
        messages=[{"role": "user", "content": text}],
    )
    return "".join(block.text for block in response.content if hasattr(block, "text"))
