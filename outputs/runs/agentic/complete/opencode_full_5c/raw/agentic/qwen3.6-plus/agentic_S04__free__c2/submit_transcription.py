import sys
import json
from typing import Optional

from speech_models import TranscriptionRequest
from speech_client import submit_transcription_job, get_assemblyai_config


def submit_transcription(
    audio_file_path: str,
    language_code: Optional[str] = None,
    punctuate: bool = True,
    format_text: bool = True,
    dual_channel: bool = False,
    custom_spelling: Optional[list] = None,
) -> dict:
    config = get_assemblyai_config()
    request = TranscriptionRequest(
        audio_file_path=audio_file_path,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
        dual_channel=dual_channel,
        custom_spelling=custom_spelling,
    )
    job = submit_transcription_job(request, config)
    return {
        "job_id": job.job_id,
        "status": job.status.value,
        "audio_url": job.audio_url,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <audio_file_path> [language_code]")
        sys.exit(1)
    audio_file_path = sys.argv[1]
    language_code = sys.argv[2] if len(sys.argv) > 2 else None
    result = submit_transcription(
        audio_file_path=audio_file_path,
        language_code=language_code,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
