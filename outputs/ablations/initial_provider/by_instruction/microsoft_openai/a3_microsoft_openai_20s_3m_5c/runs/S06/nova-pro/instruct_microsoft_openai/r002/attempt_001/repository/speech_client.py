from azure.cognitiveservices.speech import SpeechConfig

def get_speech_config():
    speech_key, service_region = "YOUR_SPEECH_KEY", "YOUR_SERVICE_REGION"
    return SpeechConfig(subscription=speech_key, region=service_region)