import os
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, speech_synthesis_voice_name='en-US-GuyNeural')

def generate_audio_brief(text):
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception('Speech synthesis failed')