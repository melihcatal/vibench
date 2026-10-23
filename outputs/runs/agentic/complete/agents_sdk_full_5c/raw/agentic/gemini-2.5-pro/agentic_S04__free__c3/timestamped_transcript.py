import time
from speech_client import get_assemblyai_session
from speech_models import WordTimestamp

def request_timestamped_transcript(audio_url: str) -> list[WordTimestamp]:
    """
    Submits a transcription job with word timestamps enabled and returns
    the word-level timestamps.
    """
    session = get_assemblyai_session()
    transcript_url = "https://api.assemblyai.com/v2/transcript"

    payload = {
        "audio_url": audio_url,
        "word_timestamps": True,
    }

    response = session.post(transcript_url, json=payload)
    response.raise_for_status()
    job_id = response.json()["id"]

    result_url = f"{transcript_url}/{job_id}"
    while True:
        result_response = session.get(result_url)
        result_response.raise_for_status()
        result = result_response.json()
        if result['status'] == 'completed':
            return [WordTimestamp(**w) for w in result.get('words', [])]
        elif result['status'] == 'error':
            raise Exception(f"Transcription failed: {result['error']}")
        time.sleep(3)
