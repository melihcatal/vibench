import argparse
import json
import os
import sys
import threading

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--language", default="en-US")
    parser.add_argument("--punctuate", action="store_true")
    parser.add_argument("--api-key", default=os.environ.get("ASSEMBLYAI_API_KEY"))
    return parser.parse_args()


def stream_transcript(api_key, media_url, language, punctuate):
    headers = {"authorization": api_key, "content-type": "application/json"}
    create_resp = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": media_url, "language_code": language, "punctuate": punctuate},
        timeout=30,
    )
    create_resp.raise_for_status()
    transcript_id = create_resp.json()["id"]
    stop_event = threading.Event()

    def poll():
        while not stop_event.is_set():
            resp = requests.get(
                f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            if data["status"] == "completed":
                print(data.get("text", ""))
                stop_event.set()
            elif data["status"] == "error":
                raise RuntimeError(data.get("error", "transcription failed"))
            else:
                print(data.get("text", ""), flush=True)
            stop_event.wait(2)

    thread = threading.Thread(target=poll, daemon=True)
    thread.start()
    thread.join()


def main():
    args = parse_args()
    if not args.api_key:
        raise SystemExit("ASSEMBLYAI_API_KEY is required")
    stream_transcript(args.api_key, args.url, args.language, args.punctuate)


if __name__ == "__main__":
    main()
