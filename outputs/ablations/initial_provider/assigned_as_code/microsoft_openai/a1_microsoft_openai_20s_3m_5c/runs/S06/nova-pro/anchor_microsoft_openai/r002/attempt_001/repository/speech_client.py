import azure.cognitiveservices.speech as speechsdk

def get_speech_config(config):
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_synthesis_voice_name = config.get('voice', 'en-US-JennyNeural')
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    return speech_config