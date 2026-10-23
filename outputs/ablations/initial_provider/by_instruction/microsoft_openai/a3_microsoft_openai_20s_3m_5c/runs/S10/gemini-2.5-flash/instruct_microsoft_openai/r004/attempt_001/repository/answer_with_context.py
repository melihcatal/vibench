import os
from openai import OpenAI

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (OpenAI) to answer a question using provided context.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    response = client.chat.completions.create(
        model="gpt-4o", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}\nAnswer:"}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content