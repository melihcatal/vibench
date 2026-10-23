from openai import OpenAI

from speech_client import openai_client_kwargs


def archive_summary(transcript_text: str):
    client = OpenAI(**openai_client_kwargs())
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcription for archival metadata:\n{transcript_text}",
            }
        ],
    )
    return response.choices[0].message.content
