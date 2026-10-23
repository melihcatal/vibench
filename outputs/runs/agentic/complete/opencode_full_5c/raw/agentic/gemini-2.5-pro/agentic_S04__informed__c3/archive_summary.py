import os
from openai import OpenAI


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a transcript using OpenAI's Chat Completions API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes transcripts.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following transcript:\n\n{transcript_text}",
            },
        ],
    )

    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content.strip()
    return ""
