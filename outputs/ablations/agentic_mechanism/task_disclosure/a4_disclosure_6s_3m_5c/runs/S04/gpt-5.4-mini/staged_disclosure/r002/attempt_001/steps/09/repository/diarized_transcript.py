import json
import os
import sys
from pathlib import Path

from assemblyai import Transcriber, TranscriptionConfig


def main() -> int:
    if len(sys.argv) < 2:
        return 1
    audio_path = Path(sys.argv[1])
    if not audio_path.exists():
        return 1
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        return 1
    os.environ["ASSEMBLYAI_API_KEY"] = api_key
    transcriber = Transcriber()
    config = TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(str(audio_path), config=config)
    utterances = []
    for utterance in getattr(transcript, "utterances", []) or []:
        utterances.append({"speaker": utterance.speaker, "text": utterance.text, "start": utterance.start, "end": utterance.end})
    print(json.dumps({"text": transcript.text, "utterances": utterances}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
