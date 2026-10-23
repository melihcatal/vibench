import os
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def generate_spoken_brief(text):
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, speech_synthesis_voice_name="en-US-JennyNeural"
    )
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(result.reason)
