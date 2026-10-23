import os
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResult, Segment, Word


def get_timestamped_transcript(
    audio_file_url: str, language: str = "en-US"
) -> TranscriptionResult:
    client = SpeechClient()
    speech_config = client.get_speech_config()

    # In a real Azure Batch Speech-to-Text scenario, you would submit a request
    # with word-level timestamps enabled. The result would then include timestamp
    # information for each word.
    # For this example, we simulate a timestamped result based on the mock data.

    print(f"Requesting timestamped transcript for {audio_file_url}")

    # Simulate a job submission
    job_id = f"mock_timestamp_job_{os.urandom(4).hex()}"
    print(f"Simulated timestamped job submitted. Job ID: {job_id}")

    # Simulate polling and getting results with word-level timestamps
    # A real implementation would poll the Azure API for the job status
    # and then retrieve the timestamped transcription.
    mock_segments = [
        Segment(
            text="The quick brown fox",
            offset=0,
            duration=2000,
            words=[
                Word(word="The", offset=0, duration=200),
                Word(word="quick", offset=200, duration=400),
                Word(word="brown", offset=600, duration=600),
                Word(word="fox", offset=1200, duration=800),
            ],
        ),
        Segment(
            text="jumps over the lazy dog.",
            offset=2500,
            duration=3500,
            words=[
                Word(word="jumps", offset=2500, duration=500),
                Word(word="over", offset=3000, duration=400),
                Word(word="the", offset=3400, duration=200),
                Word(word="lazy", offset=3600, duration=600),
                Word(word="dog.", offset=4200, duration=1800),
            ],
        ),
    ]

    return TranscriptionResult(
        job_id=job_id, status="Completed", segments=mock_segments
    )
