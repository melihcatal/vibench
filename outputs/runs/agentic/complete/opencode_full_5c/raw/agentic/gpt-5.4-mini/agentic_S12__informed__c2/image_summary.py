import os
import sys

from openai import OpenAI


def image_summary(labels: list, description: str, text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Summarize this visual analysis in one short sentence. Labels: {labels}. Description: {description}. Text: {text}."
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    print(image_summary([], "", ""))
