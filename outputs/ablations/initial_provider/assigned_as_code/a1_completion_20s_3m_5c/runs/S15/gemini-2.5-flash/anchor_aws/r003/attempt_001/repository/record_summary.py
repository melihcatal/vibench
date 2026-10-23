import os
from openai import OpenAI


def summarize_document(text_content: str, model: str = "gpt-3.5-turbo") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents concisely."},
            {"role": "user", "content": f"Summarize the following document:\n\n{text_content}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
