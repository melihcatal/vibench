from model_client import get_client, get_model


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    completion = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "Answer using only the provided context."},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return completion.choices[0].message.content
