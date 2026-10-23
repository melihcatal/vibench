from azure.ai.speech import SpeechConfig, SpeechRecognizer

def transcribe_audio(audio_bytes, config):
    speech_config = SpeechConfig(subscription=config['api_key'], region=config['region'])
    recognizer = SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once_async(audio_data=audio_bytes).get()
    return result.text