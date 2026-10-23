from model_client import create_client, model_name


def answer_with_context(question: str, context: str) -> str:
    client = create_client()
    response = client.chat.completions.create(
        model=model_name(),
        messages=[
            {"role": "system", "content": "Answer only using the provided context."},
            {"role": "user", "content": f"Context:
{context}

Question:
{question}"},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content
