from model_client import get_client, get_model_family, normalize_text


def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_family("gpt-4.1-mini"),
        messages=[
            {
                "role": "system",
                "content": "Answer using only the provided context when possible.",
            },
            {
                "role": "user",
                "content": f"Context:\n{normalize_text(context)}\n\nQuestion:\n{normalize_text(question)}",
            },
        ],
    )
    return response.choices[0].message.content or ""
