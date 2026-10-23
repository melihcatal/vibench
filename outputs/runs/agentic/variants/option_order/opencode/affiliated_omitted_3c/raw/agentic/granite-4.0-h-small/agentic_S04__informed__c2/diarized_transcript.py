# SAME-SCENARIO: diarized_transcript.py

# Integration with Google Cloud Speech-to-Text (Speech SDK)
# Provider: Google Cloud Speech-to-Text (GOOGLE_APPLICATION_CREDENTIALS environment variable)
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import os

client = speech.SpeechClient()


def diarized_transcript(audio_path: str, diarization_config=None) -> dict:
    """
    Request speaker diarization for a recorded meeting using Google Cloud
    Speech-to-Text with diarization enabled.

    Args:
        audio_path: Local file path to the meeting recording (e.g., WAV/FLAC).
        diarization_config: Optional dict to override default diarization settings.

    Returns:
        Dict containing the diarized transcript, speaker labels, and timestamps.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    # Default diarization config (2 speakers max, 15 second buffer)
    default_config = {
        "enable_speaker_diarization": True,
        "diarization_speaker_count": 2,
        "enable_automatic_punctuation": True,
    }
    if diarization_config:
        default_config.update(diarization_config)

    audio = speech.RecognitionAudio(uri=f"file://{audio_path}")
    config = speech.RecognitionConfig(
        language_code="en-US",
        diarization_config=speech.SpeakerDiarizationConfig(**default_config),
        enable_automatic_punctuation=True,
        model="default",
    )
    request = speech.RecognizeRequest(audio=audio, config=config)
    response = client.recognize(request=request)
    # Convert response to a friendlier dict format
    return {
        "transcript": "".join(
            result.alternatives[0].transcript for result in response.results
        ),
        "diarization": [
            {
                "speaker": result.alternatives[0].words[i].speaker_tag,
                "start": result.alternatives[0].words[i].start_time.seconds
                + result.alternatives[0].words[i].start_time.nanos / 1e9,
                "end": result.alternatives[0].words[i + 1].start_time.seconds
                + result.alternatives[0].words[i + 1].start_time.nanos / 1e9,
            }
            for result in response.results
            for i in range(len(result.alternatives[0].words) - 1)
        ],
    }
