import os
import openai

def answer_with_context(question: str, context: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.api_base,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": f"Using the following context, answer the question. Context: {context}\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content
