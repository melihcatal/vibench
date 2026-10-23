import os
import azure.cognitiveservices.speech as speechsdk
from typing import Optional


def generate_spoken_brief(
    text: str, output_file: str = "output.wav", voice_name: Optional[str] = None
) -> bool:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables are required"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )

    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    else:
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}")

    return False
