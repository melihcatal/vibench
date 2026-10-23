import os
from speech_client import get_assemblyai_client
from speech_models import DiarizedTranscriptRequest, DiarizedTranscriptResponse


def request_diarized_transcript(audio_url: str) -> DiarizedTranscriptResponse:
    """
    Requests a diarized transcript from AssemblyAI.
    """
    client = get_assemblyai_client()
    diarize_request = DiarizedTranscriptRequest(audio_url=audio_url)
    response_data = client.submit_transcription(
        diarize_request.audio_url, speaker_labels=True
    )
    return DiarizedTranscriptResponse(**response_data)


if __name__ == "__main__":
    # This is an example, replace with a real audio url for a meeting
    meeting_audio_url = "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a"
    if "ASSEMBLYAI_API_KEY" not in os.environ:
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    else:
        diarization_response = request_diarized_transcript(meeting_audio_url)
        print(f"Diarization job submitted with ID: {diarization_response.id}")
        # To get the result, you would poll using the poll_transcription.py script
        # with the ID above, but parse the 'utterances' field from the final result.
