import argparse
import os
import sys

from openai import OpenAI


def submit_batch_transcription(audio_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )
    return result.text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    args = parser.parse_args()

    try:
        text = submit_batch_transcription(args.audio_path)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
