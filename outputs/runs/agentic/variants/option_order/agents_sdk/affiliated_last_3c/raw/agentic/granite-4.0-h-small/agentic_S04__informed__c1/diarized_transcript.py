import os
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResponse

# Config (env var or config file)
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')


def request_diarized_transcription(file_path: str, speaker_count: int = 2) -> str:
    """Submit audio for batch transcription with speaker diarization."""
    client = SpeechClient(api_key=ASSEMBLYAI_API_KEY)
    # Upload audio (returns remote URL used by provider)
    audio_url = client.upload_audio(file_path)
    payload = {
        "audio_url": audio_url,
        "diarization": f"{speaker_count} speakers"
    }
    response = client.submit_transcription(payload)
    resp_obj = TranscriptionResponse(response)
    if resp_obj:
        print(f"Diarized transcription submitted, job ID: {resp_obj.job_id}")
        return resp_obj.job_id
    else:
        raise RuntimeError(f"Failed to submit diarized transcription: {response}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio file for diarized batch transcription.")
    parser.add_argument("file", help="Audio file path.")
    parser.add_argument("--speakers", type=int, default=2, help="Number of speakers to detect.")
    args = parser.parse_args()
    job_id = request_diarized_transcription(args.file, speaker_count=args.speakers)
    print(f"Submitted job ID: {job_id}")
