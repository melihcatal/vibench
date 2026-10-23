from speech_client import OpenAIHttpClient
from speech_models import normalize_segments


def diarized_transcript(audio_path: str) -> dict:
    client = OpenAIHttpClient()
    with open(audio_path, "rb") as audio_file:
        response = client.post(
            "/audio/transcriptions",
            files={"file": audio_file},
            json={"model": client.config.openai_transcription_model, "response_format": "verbose_json", "timestamp_granularities": ["segment"]},
        )
    response.raise_for_status()
    data = response.json()
    return {"text": data.get("text", ""), "segments": normalize_segments(data)}
