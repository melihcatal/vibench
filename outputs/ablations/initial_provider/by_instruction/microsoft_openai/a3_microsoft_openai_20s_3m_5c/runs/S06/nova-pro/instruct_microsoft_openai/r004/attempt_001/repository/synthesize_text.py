from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream

def synthesize_text(text: str) -> AudioDataStream:
    speech_key = "YOUR_AZURE_SPEECH_KEY"
    service_region = "YOUR_AZURE_SPEECH_REGION"

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(text).get()
    return result