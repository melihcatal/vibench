import argparse
import json
import os
import sys
from openai import OpenAI


def submit_transcription(audio_path: str, model: str = "whisper-1") -> dict:
    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(model=model, file=audio_file)
    result = transcription.model_dump() if hasattr(transcription, "model_dump") else transcription
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit an audio file for batch transcription using OpenAI.")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--model", default="whisper-1", help="OpenAI transcription model to use")
    args = parser.parse_args()

    if not os.path.isfile(args.audio_file):
        print(f"File not found: {args.audio_file}", file=sys.stderr)
        return 1

    try:
        result = submit_transcription(args.audio_file, args.model)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
