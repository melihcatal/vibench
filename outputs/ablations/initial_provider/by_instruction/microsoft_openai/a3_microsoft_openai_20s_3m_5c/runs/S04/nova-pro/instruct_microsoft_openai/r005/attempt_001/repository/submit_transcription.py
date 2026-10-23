from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechRecognitionLanguage
from azure.cognitiveservices.speech.audio import AudioConfig

def submit_transcription(audio_file_path, subscription_key, region):
    speech_config = SpeechConfig(subscription=subscription_key, region=region)
    audio_config = AudioConfig(filename=audio_file_path)
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None