import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request


def submit_transcription(audio_path: str, model: str = "gpt-4o-transcribe") -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    payload = {
        "model": model,
        "input": [
            {
                "type": "input_audio",
                "input_audio": {
                    "data": base64.b64encode(audio_bytes).decode("ascii"),
                    "format": os.path.splitext(audio_path)[1].lstrip(".").lower() or "mp3",
                },
            }
        ],
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API request failed: {e.code} {body}") from e


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit an audio file for batch transcription using OpenAI.")
    parser.add_argument("audio_file")
    parser.add_argument("--model", default="gpt-4o-transcribe")
    args = parser.parse_args()

    result = submit_transcription(args.audio_file, args.model)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
