from model_client import get_client, get_config


def answer_with_context(question: str, context: str) -> str:
    config = get_config()
    client = get_client()
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {
                "role": "system",
                "content": "Answer the question using only the provided context.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
        temperature=config.temperature,
        max_tokens=config.max_output_tokens,
    )
    return response.choices[0].message.content or ""
