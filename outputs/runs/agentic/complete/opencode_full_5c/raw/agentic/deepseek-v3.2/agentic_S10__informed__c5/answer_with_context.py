import os
from openai import OpenAI


def answer_with_context(question: str, context: str) -> str:
    """
    Answer a question using provided context via OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
