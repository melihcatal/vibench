from model_client import load_config, make_client


def answer_with_context(context: str, question: str) -> str:
    config = load_config("answer")
    client = make_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Answer questions using only the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
