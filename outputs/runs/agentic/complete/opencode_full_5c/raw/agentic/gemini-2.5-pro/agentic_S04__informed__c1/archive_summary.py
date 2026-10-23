import os
from openai import OpenAI


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes transcription results using OpenAI GPT models.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to summarize meeting transcripts.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following transcript:\n\n{transcript_text}",
            },
        ],
        temperature=0.5,
        max_tokens=250,
    )

    summary = response.choices[0].message.content
    return summary if summary else ""
