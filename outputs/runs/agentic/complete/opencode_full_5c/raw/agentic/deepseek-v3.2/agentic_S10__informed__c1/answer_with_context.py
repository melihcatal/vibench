import os
from model_client import get_openai_client


def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context with OpenAI GPT model."""
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based only on the provided context. If the answer cannot be found in the context, say 'I cannot answer based on the provided context.'",
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer based only on the context above:",
            },
        ],
        max_tokens=200,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
