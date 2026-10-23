from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def get_speech_client(subscription_key: str, region: str):
    config = SpeechConfig(subscription=subscription_key, region=region)
    return SpeechSynthesizer(speech_config=config)