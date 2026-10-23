from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig

def synthesize_ssml(ssml: str) -> bytes:
    speech_key, service_region = "YOUR_SPEECH_KEY", "YOUR_SERVICE_REGION"
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_ssml_async(ssml).get()
    return result.audio_data