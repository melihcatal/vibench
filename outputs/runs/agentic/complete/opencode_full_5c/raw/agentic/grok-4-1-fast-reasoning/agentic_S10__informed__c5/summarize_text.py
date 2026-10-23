import os
from openai import OpenAI
from model_client import summarize_prompt


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = summarize_prompt(text)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
