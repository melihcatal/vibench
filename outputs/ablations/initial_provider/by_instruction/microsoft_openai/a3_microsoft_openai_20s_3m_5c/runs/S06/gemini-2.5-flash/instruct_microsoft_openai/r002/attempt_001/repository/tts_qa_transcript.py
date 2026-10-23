import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_recognizer

def transcribe_audio_for_qa(audio_bytes: bytes) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Azure Speech-to-Text.
    """
    # Azure Speech SDK's SpeechRecognizer typically takes audio from a file or a stream.
    # To use audio_bytes, we need to create an in-memory audio input stream.
    audio_config = speechsdk.audio.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
    speech_recognizer = get_speech_recognizer()

    # Push the audio bytes to the stream
    stream = speechsdk.audio.PushAudioInputStream()
    stream.write(audio_bytes)
    stream.close()

    # Re-initialize recognizer with the stream for this specific transcription
    speech_key = os.environ.get('SPEECH_KEY')
    service_region = os.environ.get('SPEECH_REGION')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer_stream = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer_stream.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech recognition canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Speech recognition failed: {result.reason}")
