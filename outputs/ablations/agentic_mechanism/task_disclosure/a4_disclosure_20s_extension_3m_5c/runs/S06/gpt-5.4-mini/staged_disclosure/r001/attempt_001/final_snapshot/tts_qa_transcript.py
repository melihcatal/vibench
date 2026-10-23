import os
from pathlib import Path

from openai import OpenAI


def transcribe_tts_sample(audio_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )
    return result.text


def main() -> None:
    audio_path = os.environ.get("TTS_QA_AUDIO_PATH")
    if not audio_path:
        raise RuntimeError("TTS_QA_AUDIO_PATH is required")
    transcript = transcribe_tts_sample(audio_path)
    output_path = os.environ.get("TTS_QA_TRANSCRIPT_PATH")
    if output_path:
        Path(output_path).write_text(transcript, encoding="utf-8")
    else:
        print(transcript)


if __name__ == "__main__":
    main()
