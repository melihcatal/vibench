import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat

def synthesize_text(text: str) -> bytes:
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, speech_synthesis_output_format=SpeechSynthesisOutputFormat.Raw16Khz16BitMonoPcm)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data