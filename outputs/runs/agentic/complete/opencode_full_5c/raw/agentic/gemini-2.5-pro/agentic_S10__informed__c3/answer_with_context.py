from model_client import get_openai_client
from model_models import Message


def answer_with_context(question: str, context: str) -> str:
    client = get_openai_client()

    prompt = f"Based on the context below, please answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"

    messages = [
        Message(
            role="system",
            content="You are a helpful assistant that answers questions based on provided context.",
        ),
        Message(role="user", content=prompt),
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[msg.dict() for msg in messages],
    )

    if response.choices:
        return response.choices[0].message.content
    return ""
