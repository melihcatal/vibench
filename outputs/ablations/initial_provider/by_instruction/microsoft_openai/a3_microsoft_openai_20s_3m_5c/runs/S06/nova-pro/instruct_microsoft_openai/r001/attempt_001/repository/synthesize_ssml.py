import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream

def synthesize_ssml(ssml: str) -> AudioDataStream:
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_ssml_async(ssml).get()
    return result