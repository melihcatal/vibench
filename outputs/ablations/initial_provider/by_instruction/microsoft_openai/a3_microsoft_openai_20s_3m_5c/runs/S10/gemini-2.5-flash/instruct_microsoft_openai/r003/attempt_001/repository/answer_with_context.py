import os
from openai import OpenAI

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (OpenAI's GPT-3.5 Turbo) to answer a question using provided context.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Use the following context to answer the user's question.\n\nContext: {context}"},
            {"role": "user", "content": question}
        ],
        max_tokens=200,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
