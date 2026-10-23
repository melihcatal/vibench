from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechRecognitionLanguage

def create_speech_config(subscription_key, region):
    return SpeechConfig(subscription=subscription_key, region=region)