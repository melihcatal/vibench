import os

from openai import OpenAI


def tts_qa_transcript(payload, config=None):
    data = dict(payload or {})
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    transcription = client.audio.transcriptions.create(
        model=data.get("model", "whisper-1"),
        file=data["audio_file"],
    )
    return {"transcript": transcription.text, "model": data.get("model", "whisper-1")}
