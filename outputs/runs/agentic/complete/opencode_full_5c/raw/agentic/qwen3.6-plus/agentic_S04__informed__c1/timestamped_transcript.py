import requests
import time
from speech_client import load_config, AssemblyAIConfig, ASSEMBLYAI_API_BASE
from speech_models import (
    TranscriptionResult,
    parse_transcription_result,
    WordInfo,
)


def get_timestamped_transcript(
    audio_url: str,
    config: AssemblyAIConfig = None,
    granularity: str = "word",
) -> list:
    if config is None:
        config = load_config()

    if not audio_url.startswith("http"):
        upload_response = requests.post(
            f"{ASSEMBLYAI_API_BASE}/upload",
            headers=config.headers(),
            data=open(audio_url, "rb"),
        )
        audio_url = upload_response.json()["upload_url"]

    payload = {
        "audio_url": audio_url,
        "language_code": config.language_code,
        "punctuate": config.punctuate,
        "format_text": config.format_text,
        "word_boost": [],
    }

    submit_response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/transcript",
        json=payload,
        headers=config.headers(),
    )
    job_data = submit_response.json()
    job_id = job_data["id"]

    poll_url = f"{ASSEMBLYAI_API_BASE}/transcript/{job_id}"
    attempts = 0
    while attempts < config.max_poll_attempts:
        response = requests.get(poll_url, headers=config.headers())
        data = response.json()
        status = data.get("status", "unknown")

        if status == "completed":
            result = parse_transcription_result(data)
            if granularity == "word":
                return [
                    {
                        "text": w.text,
                        "start_ms": w.start_ms,
                        "end_ms": w.end_ms,
                        "confidence": w.confidence,
                        "speaker": w.speaker,
                    }
                    for w in result.words
                ]
            else:
                return [
                    {
                        "text": u.text,
                        "start_ms": u.start_ms,
                        "end_ms": u.end_ms,
                        "confidence": u.confidence,
                        "speaker": u.speaker,
                    }
                    for u in result.utterances
                ]
        elif status == "error":
            raise RuntimeError(
                f"AssemblyAI timestamped transcription failed: {data.get('error')}"
            )

        attempts += 1
        time.sleep(config.poll_interval_seconds)

    raise TimeoutError("AssemblyAI timestamped transcription polling timed out")


if __name__ == "__main__":
    import sys
    import json

    audio_source = (
        sys.argv[1] if len(sys.argv) > 1 else "https://example.com/meeting.wav"
    )
    timestamps = get_timestamped_transcript(audio_source, granularity="word")
    print(json.dumps(timestamps[:5], indent=2))
