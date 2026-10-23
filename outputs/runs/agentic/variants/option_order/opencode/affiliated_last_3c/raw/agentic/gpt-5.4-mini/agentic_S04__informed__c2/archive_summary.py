import os

from openai import OpenAI


def archive_summary(transcript_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize transcription results for archival purposes.",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    return response.choices[0].message.content
