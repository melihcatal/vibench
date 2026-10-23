import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

class AudioGenerator:
    def __init__(self):
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.service_region = os.getenv('AZURE_SPEECH_REGION')
        self.speech_config = SpeechConfig(subscription=self.speech_key, region=self.service_region)
        self.synthesizer = SpeechSynthesizer(speech_config=self.speech_config)
    
    def generate_audio(self, text):
        result = self.synthesizer.speak_text_async(text).get()
        if result.reason == SpeechSynthesisResultReason.SynthesizedToAudio:
            with open('output.wav', 'wb') as audio_file:
                audio_file.write(result.audio_data)
            return 'output.wav'
        else:
            return 'Audio generation failed'

audio_generator = AudioGenerator()

def generate_spoken_brief(text):
    return audio_generator.generate_audio(text)