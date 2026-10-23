import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))

def generate_audio_brief(text):
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == SpeechSynthesisResultReason.SynthesizedToAudio:
        with open('output.wav', 'wb') as audio_file:
            audio_file.write(result.audio_data)