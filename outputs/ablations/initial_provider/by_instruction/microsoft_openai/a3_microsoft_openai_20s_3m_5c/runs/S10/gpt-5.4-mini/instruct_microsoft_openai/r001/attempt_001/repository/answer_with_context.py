from model_client import get_client, get_model_name, normalize_text


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Answer the question using only the provided context.",
            },
            {"role": "user", "content": f"Context:\n{normalize_text(context)}\n\nQuestion:\n{normalize_text(question)}"},
        ],
    )
    return response.output_text
