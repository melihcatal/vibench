from model_client import create_client, load_settings


def answer_with_context(context: str, question: str) -> str:
    settings = load_settings()
    client = create_client()
    response = client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        system="Answer the question using only the provided context.",
        messages=[
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
    )
    return "".join(block.text for block in response.content if hasattr(block, "text"))
