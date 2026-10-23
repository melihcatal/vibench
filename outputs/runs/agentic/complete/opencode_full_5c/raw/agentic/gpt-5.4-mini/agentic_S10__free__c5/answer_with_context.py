from model_client import get_openai_client, get_text_model
from model_models import normalize_text


def answer_with_context(context: str, question: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Answer using only the provided context when possible.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return normalize_text(response.output_text)
