import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_synthesizer

def synthesize_text_to_audio(text: str) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Azure Cognitive Services.
    """
    speech_synthesizer = get_speech_synthesizer()
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")

