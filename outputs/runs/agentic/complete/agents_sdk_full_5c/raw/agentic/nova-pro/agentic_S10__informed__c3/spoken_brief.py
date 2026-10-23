import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
synthesizer = SpeechSynthesizer(speech_config=speech_config)

def generate_spoken_brief(text):
    result = synthesizer.speak_text_async(text).get()
    if result.reason == SpeechSynthesisResultReason.SynthesizedToAudio:
        with open('output.wav', 'wb') as audio_file:
            audio_file.write(result.audio_data)