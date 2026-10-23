from model_client import get_openai_client, choose_chat_model


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=choose_chat_model(model),
        messages=[
            {
                "role": "system",
                "content": "Answer using only the supplied context when possible.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return response.choices[0].message.content or ""
