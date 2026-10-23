import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def tts_qa_transcript(audio_bytes, config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    audio_input = speechsdk.AudioDataStream(audio_bytes)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(stream=audio_input))
    result = recognizer.recognize_once_async().get()
    if result.reason!= speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError('Azure speech recognition failed')
    return {'transcript': result.text}
