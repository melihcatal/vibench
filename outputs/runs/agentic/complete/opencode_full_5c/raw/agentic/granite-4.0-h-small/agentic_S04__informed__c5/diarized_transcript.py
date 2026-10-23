# [SAME-SCENARIO] diarized_transcript.py
# Requests speaker diarization for a recorded meeting using Azure AI Speech SDK
import os
from azure.cognitiveservices.speech import AudioConfig, SpeechConfig, SpeechRecognizer
from speech_client import get_auth_header

SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def diarized_meeting_transcription(audio_path: str) -> dict:
    """
    Perform batch transcription with speaker diarization on a meeting recording.
    Azure AI Speech SDK is used to enable diarization.
    Returns the JSON response containing diarized text and speaker IDs.
    """
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    # Enable diarization with up to 5 speakers
    speech_config.set_property(property_id="diarization.speakerCount", value="5")
    audio_config = AudioConfig(filename=audio_path)
    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once()
    if result.reason == result.reason_other:
        if result.cancellation_details:
            raise Exception(result.cancellation_details.reason)
        raise Exception(result.reason)
    # The result contains diarization data under result.diarization_inference
    return {
        "transcript": result.text,
        "diarization": result.ai_metadata.get("diarization_inference", {}),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python diarized_transcript.py <path-to-meeting-recording>")
        sys.exit(1)
    result = diarized_meeting_transcription(sys.argv[1])
    print("Diarized transcript:", result["transcript"])
    print("Speaker IDs:", result["diarization"])
