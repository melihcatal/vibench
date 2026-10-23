import json
import os
import sys

import websocket


ASSEMBLYAI_WS_URL = "wss://api.assemblyai.com/v2/realtime/ws"


def build_url(language_code: str, punctuate: bool) -> str:
    return f"{ASSEMBLYAI_WS_URL}?sample_rate=16000&punctuate={'true' if punctuate else 'false'}&language_code={language_code}"


def main() -> None:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    language_code = os.environ.get("ASSEMBLYAI_LANGUAGE_CODE", "en_us")
    punctuate = os.environ.get("ASSEMBLYAI_PUNCTUATE", "true").lower() in {"1", "true", "yes", "on"}

    ws = websocket.create_connection(build_url(language_code, punctuate), header=[f"Authorization: {api_key}"])

    try:
        while True:
            message = ws.recv()
            if not message:
                continue
            data = json.loads(message)
            if data.get("message_type") == "FinalTranscript":
                transcript = data.get("text", "")
                if transcript:
                    sys.stdout.write(transcript + "\n")
                    sys.stdout.flush()
            elif data.get("message_type") == "SessionBegins":
                continue
    finally:
        ws.close()


if __name__ == "__main__":
    main()
