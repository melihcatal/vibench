from model_client import get_client, get_model_name


def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=get_model_name("gemini-2.0-flash"),
        contents=f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer using only the context.",
    )
    return getattr(response, "text", "")
