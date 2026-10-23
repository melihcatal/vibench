from typing import List, Dict
from speech_client import AssemblyAIClient
from poll_transcription import poll_for_transcript


def get_diarized_transcript(audio_url: str) -> List[Dict[str, str]]:
    """
    Submits a job with speaker diarization enabled and returns the diarized utterances.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of dictionaries, each containing the speaker and their spoken text.
    """
    client = AssemblyAIClient()
    print("Submitting job with speaker diarization enabled...")
    # AssemblyAI requires speaker_labels to enable diarization.
    submit_response = client.submit_transcription(audio_url, speaker_labels=True)

    print(f"Job submitted with ID: {submit_response.id}. Polling for completion...")
    completed_response = poll_for_transcript(submit_response.id)

    if not completed_response.utterances:
        print("No utterances found in the response.")
        return []

    diarized_result = [
        {"speaker": utterance.speaker, "text": utterance.text}
        for utterance in completed_response.utterances
    ]
    return diarized_result


# Example usage:
# if __name__ == '__main__':
#     # A sample audio file with multiple speakers
#     AUDIO_URL = "https://storage.googleapis.com/aai-docs-samples/sports_interview.wav"
#     diarization = get_diarized_transcript(AUDIO_URL)
#     for entry in diarization:
#         print(f"{entry['speaker']}: {entry['text']}")
