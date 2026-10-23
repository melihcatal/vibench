import os
from openai import OpenAI


def summarize_text(text: str, max_words: int = 150) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a concise summarizer. Summarize the provided text in no more than the specified number of words.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text in at most {max_words} words:\n\n{text}",
            },
        ],
        temperature=0.3,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()
