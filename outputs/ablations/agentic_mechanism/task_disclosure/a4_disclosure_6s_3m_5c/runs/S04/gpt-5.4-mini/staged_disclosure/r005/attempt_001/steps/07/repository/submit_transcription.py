import argparse
import base64
import json
import mimetypes
import os
import sys
from urllib import error, request


OPENAI_TRANSCRIPTION_MODEL = os.environ.get("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")


def submit_batch_transcription(audio_path: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    mime_type = mimetypes.guess_type(audio_path)[0] or "application/octet-stream"
    payload = {
        "model": OPENAI_TRANSCRIPTION_MODEL,
        "input": [
            {
                "type": "input_audio",
                "audio": base64.b64encode(audio_bytes).decode("ascii"),
                "format": mime_type,
                "filename": os.path.basename(audio_path),
            }
        ],
    }

    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=300) as resp:
            return json.load(resp)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file")
    args = parser.parse_args()
    result = submit_batch_transcription(args.audio_file)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
