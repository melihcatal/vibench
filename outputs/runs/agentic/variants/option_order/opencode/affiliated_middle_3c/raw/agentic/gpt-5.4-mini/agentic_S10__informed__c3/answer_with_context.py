from model_client import get_client, get_model_name


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {
                "role": "system",
                "content": "Answer using only the provided context when possible.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return response.choices[0].message.content or ""
