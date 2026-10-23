from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

def transcribe_audio(file_path: str) -> str:
    speech_key = "YOUR_AZURE_SPEECH_KEY"
    service_region = "YOUR_AZURE_SPEECH_REGION"

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    recognizer = SpeechRecognizer(speech_config=speech_config)

    result = recognizer.recognize_once_async().get()
    return result.text