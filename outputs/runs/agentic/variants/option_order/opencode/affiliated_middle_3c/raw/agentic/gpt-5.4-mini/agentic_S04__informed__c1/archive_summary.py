from openai import OpenAI
from speech_client import load_config


def archive_summary(transcript_text: str) -> str:
    client = OpenAI(api_key=load_config().api_key or "")
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize the transcription results for archival storage."},
            {"role": "user", "content": transcript_text},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
