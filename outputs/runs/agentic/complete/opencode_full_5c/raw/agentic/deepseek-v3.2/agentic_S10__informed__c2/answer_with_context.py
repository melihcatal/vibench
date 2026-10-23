import os
from openai import OpenAI


def answer_with_context(question: str, context: str) -> str:
    """
    Answer a question using provided context with OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based ONLY on the provided context. If the answer cannot be found in the context, say 'I cannot answer based on the provided context.'",
            },
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"},
        ],
        max_tokens=200,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
