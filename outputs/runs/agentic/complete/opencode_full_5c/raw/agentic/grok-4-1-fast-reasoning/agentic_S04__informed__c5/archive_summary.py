import os
from openai import OpenAI


def archive_summary(transcript: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts concisely, capturing key points, decisions, and action items.",
            },
            {
                "role": "user",
                "content": f"Summarize this transcript:\\n\\n{transcript}",
            },
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
