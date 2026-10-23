import os
import azure.cognitiveservices.speech as speechsdk

def synthesize_ssml(ssml_text: str) -> bytes:
    """
    Synthesizes SSML text to an audio byte stream using Azure AI Speech.
    """
    speech_key = os.environ.get("SPEECH_KEY")
    speech_region = os.environ.get("SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None) # None for in-memory stream

    result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}. Error details: {result.cancellation_details.error_details if result.cancellation_details else 'N/A'}")
