import requests
from speech_client import load_config, AssemblyAIConfig, ASSEMBLYAI_API_BASE
from speech_models import TranscriptionSubmission


def submit_transcription(
    audio_url: str,
    config: AssemblyAIConfig = None,
    language_code: str = None,
    punctuate: bool = None,
    format_text: bool = None,
    dual_channel: bool = None,
) -> TranscriptionSubmission:
    if config is None:
        config = load_config()

    payload = {
        "audio_url": audio_url,
        "language_code": language_code or config.language_code,
        "punctuate": punctuate if punctuate is not None else config.punctuate,
        "format_text": format_text if format_text is not None else config.format_text,
        "dual_channel": dual_channel
        if dual_channel is not None
        else config.dual_channel,
    }

    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/upload"
        if not audio_url.startswith("http")
        else f"{ASSEMBLYAI_API_BASE}/transcript",
        json=payload if audio_url.startswith("http") else None,
        headers=config.headers(),
    )

    if not audio_url.startswith("http"):
        upload_response = response.json()
        audio_url = upload_response["upload_url"]
        payload = {
            "audio_url": audio_url,
            "language_code": language_code or config.language_code,
            "punctuate": punctuate if punctuate is not None else config.punctuate,
            "format_text": format_text
            if format_text is not None
            else config.format_text,
            "dual_channel": dual_channel
            if dual_channel is not None
            else config.dual_channel,
        }
        response = requests.post(
            f"{ASSEMBLYAI_API_BASE}/transcript",
            json=payload,
            headers=config.headers(),
        )

    data = response.json()
    return TranscriptionSubmission(
        job_id=data["id"],
        status=data.get("status", "queued"),
        audio_url=audio_url,
        raw_response=data,
    )


if __name__ == "__main__":
    import sys

    audio_source = (
        sys.argv[1] if len(sys.argv) > 1 else "https://example.com/meeting.wav"
    )
    submission = submit_transcription(audio_source)
    print(f"Job ID: {submission.job_id}")
    print(f"Status: {submission.status}")
