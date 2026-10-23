import os
from openai import OpenAI


def summarize_rotation_status(rotation_notes: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes technical notes concisely.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following secret rotation status notes:\n\n{rotation_notes}",
            },
        ],
    )
    if completion.choices:
        return completion.choices[0].message.content
    return ""
