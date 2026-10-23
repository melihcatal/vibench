import os
from openai import OpenAI


def answer_with_context(context: str, question: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the user's question using only the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
    )
    return response.choices[0].message.content or ""
