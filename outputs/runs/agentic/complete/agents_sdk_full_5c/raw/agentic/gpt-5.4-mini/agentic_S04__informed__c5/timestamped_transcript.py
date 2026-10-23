from __future__ import annotations

from typing import Any, Dict, List

from speech_client import create_client


def timestamped_transcript(audio_file: str) -> Dict[str, List[dict]]:
    transcriber = create_client()
    transcript = transcriber.transcribe(audio_file, config=None)
    return {
        "words": list(getattr(transcript, "words", []) or []),
        "utterances": list(getattr(transcript, "utterances", []) or []),
    }


if __name__ == "__main__":
    raise SystemExit("import and call timestamped_transcript(audio_file)")
