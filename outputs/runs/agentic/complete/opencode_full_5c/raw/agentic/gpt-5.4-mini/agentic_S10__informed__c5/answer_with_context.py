from model_client import get_client, pick_model


def answer_with_context(question, context, model=None):
    client = get_client()
    response = client.chat.completions.create(
        model=pick_model(model),
        messages=[
            {"role": "system", "content": "Answer using only the provided context."},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
        temperature=0.2,
        max_tokens=256,
    )
    return response.choices[0].message.content
