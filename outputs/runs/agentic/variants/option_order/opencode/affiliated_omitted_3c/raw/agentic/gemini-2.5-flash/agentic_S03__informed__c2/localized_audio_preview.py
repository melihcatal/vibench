import os
import azure.cognitiveservices.speech as speechsdk
from translation_models import AudioPreviewRequest
import dataclasses

@dataclasses.dataclass
class AudioPreviewResponse:
    audio_content: bytes

def generate_localized_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_language = request.language
    speech_config.speech_synthesis_voice_name = request.voice_name

    # Use the default speaker output for synthesis, then read the audio data
    audio_config = speechsdk.audio.AudioOutputConfig(use_ Alberton_as_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None) # No explicit audio_config to capture stream

    result = speech_synthesizer.speak_text_async(request.text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return AudioPreviewResponse(audio_content=audio_data)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception("Speech synthesis failed for an unknown reason.")
