import os

from openai import OpenAI

from speech_models import TranscriptArtifact, join_segments


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def archive_summary(artifact: TranscriptArtifact) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = artifact.transcript or join_segments(artifact.segments)
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "Produce a concise archive summary of the meeting transcript."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
