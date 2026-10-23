import os
from openai import OpenAI


def summarize_record(text_content: str):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text_content}",
            },
        ],
        temperature=0.5,
    )
    summary = response.choices[0].message.content
    return summary.strip() if summary else ""
