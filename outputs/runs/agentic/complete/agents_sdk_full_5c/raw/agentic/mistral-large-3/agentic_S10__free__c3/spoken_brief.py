import os
from typing import Optional
import azure.cognitiveservices.speech as speechsdk

def generate_spoken_brief(text: str, output_file: Optional[str] = None) -> Optional[str]:
    """Generate a spoken brief from the model output using Azure Speech Service."""
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION")
    )
    audio_config = None
    if output_file:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return output_file if output_file else "Speech synthesized to speaker."
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")