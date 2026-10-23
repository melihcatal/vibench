import json
from speech_client import BatchSTTClient


def request_diarized_transcription(audio_path, num_speakers=2, language="en-US"):
    """Request a batch transcription with speaker diarization.

    Args:
        audio_path (str): Path to the audio file.
        num_speakers (int): Expected number of speakers.
        language (str): Language code.

    Returns:
        dict: Response payload (job ID) from the provider.
    """
    client = BatchSTTClient()
    payload = {
        "audio": audio_path,
        "language": language,
        "diarization": {"enable": True, "speaker_count": num_speakers},
    }
    response = client.submit_batch_job(payload)
    return response


# Example (uncomment to test)
# if __name__ == "__main__":
#     resp = request_diarized_transcription("meeting.wav", num_speakers=4)
#     print(json.dumps(resp, indent=2))
