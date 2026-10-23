from openai import OpenAI

from model_client import resolve_model


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=resolve_model(model),
        input=f"Answer the question using only the provided context.\nContext:\n{context}\nQuestion:\n{question}",
    )
    return response.output_text
