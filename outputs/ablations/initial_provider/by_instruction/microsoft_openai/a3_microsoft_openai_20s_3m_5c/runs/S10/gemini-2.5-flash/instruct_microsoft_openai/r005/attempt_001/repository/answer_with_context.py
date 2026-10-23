import os
from openai import OpenAI

def answer_with_context(question: str, context: str) -> str:
    """
    Answers a question using the provided context with a hosted OpenAI LLM.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another suitable OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
