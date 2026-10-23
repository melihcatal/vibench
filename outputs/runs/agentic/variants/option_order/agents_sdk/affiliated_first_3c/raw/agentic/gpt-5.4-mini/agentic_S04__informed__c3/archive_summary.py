import os

from openai import OpenAI


def archive_summary(transcript_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize transcription results for archival records."},
            {"role": "user", "content": transcript_text},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
