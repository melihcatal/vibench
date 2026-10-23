import os
from speech_client import load_config, openai_post


def diarized_transcript(audio_path: str):
    config = load_config()
    with open(audio_path, "rb") as f:
        response = openai_post(
            config,
            "/audio/transcriptions",
            data={"model": config.openai_transcription_model, "response_format": "verbose_json", "timestamp_granularities[]": "segment"},
            files={"file": f},
        )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print(diarized_transcript(os.environ.get("AUDIO_PATH", "meeting.wav")))
