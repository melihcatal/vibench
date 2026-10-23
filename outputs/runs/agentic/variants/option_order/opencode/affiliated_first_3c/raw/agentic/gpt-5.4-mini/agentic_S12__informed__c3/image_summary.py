import os

from openai import OpenAI


def image_summary(labels: str, description: str, text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize visual analysis. Labels: {labels}. Description: {description}. Text: {text}."
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
