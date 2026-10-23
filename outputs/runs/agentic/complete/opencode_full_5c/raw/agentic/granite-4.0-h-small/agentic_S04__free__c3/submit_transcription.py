# submit_transcription.py

from speech_client import get_speech_client


def submit_transcription(file_path, language="en-US"):
    client = get_speech_client()
    response = client.submit_batch_transcription(
        audio_file=file_path,
        language_code=language,
        features={"diarization": False, "timestamps": False},
    )
    return response["job_id"]


if __name__ == "__main__":
    import sys, json

    job_id = submit_transcription(
        sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "en-US"
    )
    print(json.dumps({"job_id": job_id}))
