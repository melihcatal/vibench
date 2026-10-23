import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_localized_audio_preview(text, language):
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, language=language)
    result = synthesizer.speak_text_async(text).get()
    with open('output.wav', 'wb') as audio_file:
        audio_file.write(result.audio_data)