from model_client import get_client, pick_model


def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    model = pick_model("answer")
    resp = client.chat.completions.create(
        model=model,
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
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
