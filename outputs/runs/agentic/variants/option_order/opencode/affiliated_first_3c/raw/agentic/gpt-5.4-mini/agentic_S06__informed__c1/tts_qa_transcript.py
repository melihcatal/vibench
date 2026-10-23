import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(audio_path: str, key: str, region: str) -> str:
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once_async().get()
    return result.text
