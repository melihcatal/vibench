# timestamped_transcript.py

from speech_client import get_speech_client


def get_timestamped_transcript(job_id):
    client = get_speech_client()
    result = client.get_transcription_result(job_id, format="timestamped")
    return result["segments"]


if __name__ == "__main__":
    import sys, json

    job_id = sys.argv[1]
    segments = get_timestamped_transcript(job_id)
    print(json.dumps(segments))
