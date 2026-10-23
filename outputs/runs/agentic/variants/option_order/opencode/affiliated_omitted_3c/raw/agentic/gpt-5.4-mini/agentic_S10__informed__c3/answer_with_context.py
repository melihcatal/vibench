from model_client import choose_model, get_client


def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    response = client.chat.complete(
        model=choose_model("answer"),
        messages=[
            {
                "role": "system",
                "content": "Answer the question only using the provided context.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return response.choices[0].message.content
