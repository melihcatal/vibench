from openai import OpenAI
from speech_models import TranscriptionResult

def archive_summary(transcript: str) -> str:
    """Summarize transcription results using OpenAI's GPT-4."""
    client = OpenAI(api_key=open(".openai_api_key").read().strip())

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following transcript:"},
            {"role": "user", "content": transcript},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()