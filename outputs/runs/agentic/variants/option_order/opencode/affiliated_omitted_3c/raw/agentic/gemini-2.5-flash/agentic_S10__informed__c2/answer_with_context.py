import os
from openai import OpenAI

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (OpenAI) to answer a question using provided context.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Provider-specific model ID
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Use the following context to answer the question:

{context}"},
            {"role": "user", "content": question}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
