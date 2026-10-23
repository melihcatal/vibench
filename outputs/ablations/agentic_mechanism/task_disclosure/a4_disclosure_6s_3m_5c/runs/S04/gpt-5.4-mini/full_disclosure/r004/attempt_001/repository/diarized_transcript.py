import os
from openai import OpenAI


def diarized_transcript(audio_url: str, model: str = "gpt-4o-transcribe"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    transcription = client.audio.transcriptions.create(
        model=model,
        file=audio_url,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        extra_body={"diarization": True},
    )
    return transcription
