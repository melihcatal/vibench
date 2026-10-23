from __future__ import annotations

import assemblyai as aai

from speech_client import create_client, load_config
from speech_models import normalize_result


def poll_transcription(job_id: str) -> dict:
    load_config()
    transcript = aai.Transcript(job_id)
    transcript = transcript.get()  # AssemblyAI transcript retrieval
    return normalize_result(transcript).__dict__


if __name__ == "__main__":
    raise SystemExit("import and call poll_transcription(job_id)")
