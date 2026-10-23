import azure.cognitiveservices.speech as speechsdk


def synthesize_text(payload, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_synthesis_voice_name = config.get('voice', 'en-US-JennyNeural')
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_text_async(payload['text']).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure speech synthesis failed')
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
