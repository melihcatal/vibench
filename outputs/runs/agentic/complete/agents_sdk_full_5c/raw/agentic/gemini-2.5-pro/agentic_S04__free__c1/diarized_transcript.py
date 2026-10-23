from typing import List
from speech_client import post_to_assemblyai, get_from_assemblyai
from speech_models import Utterance
import time

def request_diarized_transcript(audio_url: str) -> List[Utterance]:
    """
    Requests a diarized (speaker-separated) transcript from AssemblyAI.
    """
    # Step 1: Submit the job with speaker_labels enabled
    submit_payload = {
        "audio_url": audio_url,
        "speaker_labels": True
    }
    submit_response = post_to_assemblyai("transcript", submit_payload)
    job_id = submit_response['id']

    # Step 2: Poll for completion
    while True:
        poll_response = get_from_assemblyai(f"transcript/{job_id}")
        if poll_response['status'] == 'completed':
            break
        elif poll_response['status'] == 'error':
            raise RuntimeError(f"AssemblyAI transcription failed: {poll_response['error']}")
        time.sleep(3)
    
    # Step 3: Return the utterances
    if poll_response.get("utterances"):
        return [Utterance(**u) for u in poll_response["utterances"]]
    return []
