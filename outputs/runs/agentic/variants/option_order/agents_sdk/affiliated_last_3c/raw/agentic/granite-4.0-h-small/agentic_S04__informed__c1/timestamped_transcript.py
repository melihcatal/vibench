import os
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResponse

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

def request_timestamped_transcription(file_path: str) -> str:
    """Submit request for transcription with word/segment timestamps."""
    client = SpeechClient(api_key=ASSEMBLYAI_API_KEY)
    audio_url = client.upload_audio(file_path)
    payload = {
        "audio_url": audio_url,
        "timestamps": "true"
    }
    response = client.submit_transcription(payload)
    resp_obj = TranscriptionResponse(response)
    if resp_obj:
        print(f"Timestamped transcription submitted, job ID: {resp_obj.job_id}")
        return resp_obj.job_id
    else:
        raise RuntimeError(f"Failed to submit timestamped transcription: {response}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio for timestamped transcription.")
    parser.add_argument("file", help="Path to audio file.")
    args = parser.parse_args()
    job_id = request_timestamped_transcription(args.file)
    print(f"Submitted job ID: {job_id}")
