from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from speech_client import get_client, load_config
from speech_models import build_transcription_payload


def submit_transcription(audio_path: str, *, language: Optional[str] = None, model: Optional[str] = None, webhook_url: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config = load_config()
    client = get_client(config)
    payload = build_transcription_payload(audio_path=audio_path, language=language or config.default_language, model=model or config.default_model, webhook_url=webhook_url, metadata=metadata)
    return client.transcriptions.create(payload)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    parser.add_argument("--language")
    parser.add_argument("--model")
    parser.add_argument("--webhook-url")
    args = parser.parse_args()
    result = submit_transcription(args.audio_path, language=args.language, model=args.model, webhook_url=args.webhook_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
