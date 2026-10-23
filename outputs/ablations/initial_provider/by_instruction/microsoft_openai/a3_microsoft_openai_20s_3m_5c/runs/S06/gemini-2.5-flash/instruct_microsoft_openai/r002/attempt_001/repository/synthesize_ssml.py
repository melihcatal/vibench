import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_synthesizer

def synthesize_ssml_to_audio(ssml_string: str) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls to an audio byte stream using Azure Cognitive Services.
    """
    speech_synthesizer = get_speech_synthesizer()
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")
