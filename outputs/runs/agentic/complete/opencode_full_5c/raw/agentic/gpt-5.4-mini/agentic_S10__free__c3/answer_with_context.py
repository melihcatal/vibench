from model_client import get_client, get_model


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model(),
        input=f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer using only the context.",
    )
    return resp.output_text
