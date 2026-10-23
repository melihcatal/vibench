import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config(config):
    api_key = config.get('api_key', os.getenv('AZURE_SPEECH_KEY'))
    region = config.get('region', os.getenv('AZURE_SPEECH_REGION'))
    voice = config.get('voice', 'en-US-JennyNeural')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_synthesis_voice_name = voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    return speech_config