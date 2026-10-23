import os

from openai import OpenAI

from speech_models import TranscriptArtifact, join_segments


OPENAI_MODEL = "gpt-4.1-mini"


def translate_transcript(artifact: TranscriptArtifact, target_language: str = "es") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    source_text = artifact.transcript or join_segments(artifact.segments)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"Translate transcript segments into {target_language} while preserving meaning."},
            {"role": "user", "content": source_text},
        ],
    )
    return response.choices[0].message.content or ""
