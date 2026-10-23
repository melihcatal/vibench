import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_audio_preview(text, language='es-ES'):
    speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
    synthesizer = SpeechSynthesizer(speech_config=speech_config, language=language)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        with open('output.wav', 'wb') as file:
            file.write(result.audio_data)
    else:
        print(f'Speech synthesis failed: {result.reason}')

if __name__ == '__main__':
    generate_audio_preview('Hello, world!')