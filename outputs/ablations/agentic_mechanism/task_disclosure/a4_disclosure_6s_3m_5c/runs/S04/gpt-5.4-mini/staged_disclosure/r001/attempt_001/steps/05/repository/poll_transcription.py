import argparse
import json
import os
import sys
import time

import requests


OPENAI_BATCHES_ENDPOINT = "https://api.openai.com/v1/batches/"


def get_batch(batch_id: str, api_key: str) -> dict:
    response = requests.get(
        f"{OPENAI_BATCHES_ENDPOINT}{batch_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def get_result_file(file_id: str, api_key: str) -> str:
    response = requests.get(
        f"https://api.openai.com/v1/files/{file_id}/content",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=120,
    )
    response.raise_for_status()
    return response.text


def extract_transcript(batch: dict, api_key: str) -> str | None:
    output_file_id = batch.get("output_file_id")
    if not output_file_id:
        return None
    content = get_result_file(output_file_id, api_key)
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return content
    if isinstance(payload, dict):
        if "response" in payload and isinstance(payload["response"], dict):
            response = payload["response"]
            if "body" in response and isinstance(response["body"], dict):
                body = response["body"]
                if "text" in body:
                    return body["text"]
                if "transcript" in body:
                    return body["transcript"]
        if "text" in payload:
            return payload["text"]
        if "transcript" in payload:
            return payload["transcript"]
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll an OpenAI transcription batch until completion and print the transcript.")
    parser.add_argument("batch_id", help="OpenAI batch ID to poll")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    parser.add_argument("--timeout", type=float, default=3600.0, help="Maximum polling time in seconds")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is required", file=sys.stderr)
        return 1

    deadline = time.time() + args.timeout
    while True:
        batch = get_batch(args.batch_id, api_key)
        status = batch.get("status")
        if status == "completed":
            transcript = extract_transcript(batch, api_key)
            if transcript is None:
                print("Batch completed without an output file", file=sys.stderr)
                return 1
            print(transcript)
            return 0
        if status in {"failed", "cancelled", "expired"}:
            print(json.dumps(batch, indent=2, sort_keys=True), file=sys.stderr)
            return 1
        if time.time() >= deadline:
            print("Polling timed out", file=sys.stderr)
            return 1
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
