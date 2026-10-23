import requests
import time
from speech_client import load_config, AssemblyAIConfig, ASSEMBLYAI_API_BASE
from speech_models import (
    TranscriptionResult,
    parse_transcription_result,
    TranscriptSegments,
    result_to_segments,
)


def request_diarized_transcript(
    audio_url: str,
    speaker_count: int = None,
    config: AssemblyAIConfig = None,
) -> TranscriptSegments:
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
        "speaker_labels": True,
        "dual_channel": config.dual_channel,
    }

    if speaker_count is not None:
        payload["speakers_expected"] = speaker_count
    elif config.speaker_count is not None:
        payload["speakers_expected"] = config.speaker_count

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
            return result_to_segments(result)
        elif status == "error":
            raise RuntimeError(f"AssemblyAI diarization failed: {data.get('error')}")

        attempts += 1
        time.sleep(config.poll_interval_seconds)

    raise TimeoutError("AssemblyAI diarization polling timed out")


if __name__ == "__main__":
    import sys

    audio_source = (
        sys.argv[1] if len(sys.argv) > 1 else "https://example.com/meeting.wav"
    )
    segments = request_diarized_transcript(audio_source, speaker_count=2)
    for seg in segments.segments:
        print(f"[{seg.speaker}] {seg.text}")
