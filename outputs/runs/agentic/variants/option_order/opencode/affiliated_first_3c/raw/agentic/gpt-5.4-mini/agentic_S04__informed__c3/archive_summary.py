from openai import OpenAI


def archive_summary(transcript_text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Summarize transcription results for archival.",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    return response.choices[0].message.content or ""
