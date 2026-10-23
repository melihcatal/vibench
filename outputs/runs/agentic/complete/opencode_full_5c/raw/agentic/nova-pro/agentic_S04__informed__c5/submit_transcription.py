from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer


def submit_transcription(audio_file_path):
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    speech_recognizer = SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once_async().get()
    return result.text
