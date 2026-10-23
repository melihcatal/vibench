import os
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResult, Segment, Word


def get_diarized_transcript(
    audio_file_url: str, language: str = "en-US"
) -> TranscriptionResult:
    client = SpeechClient()
    speech_config = client.get_speech_config()

    # In a real Azure Batch Speech-to-Text scenario, you would submit a request
    # with diarization enabled. The result would then include speaker information.
    # For this example, we simulate a diarized result based on the mock data.

    print(f"Requesting diarized transcript for {audio_file_url}")

    # Simulate a job submission (as in submit_transcription.py)
    job_id = f"mock_diarization_job_{os.urandom(4).hex()}"
    print(f"Simulated diarization job submitted. Job ID: {job_id}")

    # Simulate polling and getting results with speaker information
    # A real implementation would poll the Azure API for the job status
    # and then retrieve the diarized transcription.
    mock_segments = [
        Segment(
            text="Hello world,",
            offset=0,
            duration=1000,
            words=[
                Word(word="Hello", offset=0, duration=500),
                Word(word="world,", offset=500, duration=500),
            ],
            speaker=1,
        ),
        Segment(
            text="this is a test.",
            offset=1500,
            duration=1500,
            words=[
                Word(word="this", offset=1500, duration=300),
                Word(word="is", offset=1800, duration=200),
                Word(word="a", offset=2000, duration=100),
                Word(word="test.", offset=2100, duration=900),
            ],
            speaker=2,
        ),
        Segment(
            text="Speaker one continues.",
            offset=3000,
            duration=2000,
            words=[
                Word(word="Speaker", offset=3000, duration=500),
                Word(word="one", offset=3500, duration=300),
                Word(word="continues.", offset=3800, duration=1200),
            ],
            speaker=1,
        ),
    ]

    return TranscriptionResult(
        job_id=job_id, status="Completed", segments=mock_segments
    )
