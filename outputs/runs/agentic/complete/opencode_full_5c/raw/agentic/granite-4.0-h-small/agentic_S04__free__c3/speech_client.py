# speech_client.py

import os, json, logging
from dotenv import load_dotenv
from google.cloud import speechv1p1beta1 as speech

load_dotenv()

SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")
PROJECT_ID = os.getenv("SPEECH_PROJECT_ID")
REGION = os.getenv("SPEECH_REGION", "us-central1")

logging.basicConfig(level=logging.INFO)

try:
    client = speech.SpeechClient()
    client.transport.channel.host = f"{REGION}-us-speech.googleapis.com"
except Exception as e:
    logging.warning(f"Failed to create SpeechClient: {e}")


def get_speech_client():
    """Returns a configured speech client using environment credentials."""
    return client


def build_transcription_request(
    audio_file, language_code="en-US", features=None, output_format="json"
):
    """Constructs a speech API request payload for batch transcription."""
    with open(audio_file, "rb") as f:
        audio_data = f.read()
    audio = speech.RecognitionAudio(content=audio_data)
    if features is None:
        features = {}
    config = speech.RecognitionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
        diarization_config=speech.DiarizationConfig(
            enable_diarization=True, speaker_count=2
        )
        if "diarization" in features
        else None,
        metadata=speech.RecognitionMetadata(
            interaction_type=speech.RecognitionMetadata.InteractionType.DICTATION,
            microphone_distance=speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD,
        ),
    )
    return speech.BatchRecognizeRequest(
        audio=audio,
        config=config,
        output_config=speech.OutputConfig(content_type=output_format),
    )


def parse_timestamped_result(response):
    """Parse a timestamped JSON result from the API into a list of {start, end, text}."""
    results = []
    for res in response.results:
        speaker_id = res.alternatives[0].words[0].speaker_tag
        text = " ".join(w.word for w in res.alternatives[0].words)
        # approximate timestamps from words (API provides word-level timestamps)
        segment = {
            "start": res.alternatives[0].words[0].start_time.seconds
            + res.alternatives[0].words[0].start_time.nanos / 1e9,
            "end": res.alternatives[0].words[-1].end_time.seconds
            + res.alternatives[0].words[-1].end_time.nanos / 1e9,
            "text": text,
        }
        results.append(segment)
    return results
