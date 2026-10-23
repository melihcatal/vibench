from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_spoken_briefing(text):
    speech_key = "<your-speech-resource-key>"
    service_region = "<your-speech-service-region>"
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result