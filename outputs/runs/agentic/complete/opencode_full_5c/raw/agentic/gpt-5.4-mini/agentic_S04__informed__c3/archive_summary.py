from openai import OpenAI


def archive_summary(transcript_text: str):
    client = OpenAI()
    result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize transcription results concisely."},
            {"role": "user", "content": transcript_text},
        ],
    )
    return result.choices[0].message.content
