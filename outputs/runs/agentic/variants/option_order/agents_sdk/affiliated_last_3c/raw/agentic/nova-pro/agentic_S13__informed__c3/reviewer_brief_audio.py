import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

def reviewer_brief_audio(text):
    speech_config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        with open('output.wav', 'wb') as audio_file:
            audio_file.write(result.audio_data)
    else:
        print(f'Speech synthesis canceled: {result.cancellation_details.reason}')