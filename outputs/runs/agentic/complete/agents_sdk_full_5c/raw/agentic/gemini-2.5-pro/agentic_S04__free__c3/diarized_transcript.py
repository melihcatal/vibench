import time
from speech_client import get_assemblyai_session
from speech_models import Utterance

def request_diarized_transcript(audio_url: str) -> list[Utterance]:
    """
    Submits a transcription job with speaker diarization enabled and
    returns the utterances.
    """
    session = get_assemblyai_session()
    transcript_url = "https://api.assemblyai.com/v2/transcript"

    payload = {
        "audio_url": audio_url,
        "speaker_labels": True,
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
            return [Utterance(**u) for u in result.get('utterances', [])]
        elif result['status'] == 'error':
            raise Exception(f"Transcription failed: {result['error']}")
        time.sleep(3)
