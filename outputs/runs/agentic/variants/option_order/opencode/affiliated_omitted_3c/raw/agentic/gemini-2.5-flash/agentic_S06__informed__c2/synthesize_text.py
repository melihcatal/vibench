import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_synthesizer


def synthesize_text_to_audio_bytes(text: str) -> bytes:
    speech_synthesizer = get_speech_synthesizer()
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")


if __name__ == "__main__":
    # Example usage - in a real scenario, this would be called from another module
    pass
