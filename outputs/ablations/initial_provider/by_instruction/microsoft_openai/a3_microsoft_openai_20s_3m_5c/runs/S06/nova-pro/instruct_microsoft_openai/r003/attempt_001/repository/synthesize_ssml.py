import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat

def synthesize_ssml(ssml: str) -> bytes:
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, speech_synthesis_output_format=SpeechSynthesisOutputFormat.Raw16Khz16BitMonoPcm)
    result = synthesizer.speak_ssml_async(ssml).get()
    return result.audio_data