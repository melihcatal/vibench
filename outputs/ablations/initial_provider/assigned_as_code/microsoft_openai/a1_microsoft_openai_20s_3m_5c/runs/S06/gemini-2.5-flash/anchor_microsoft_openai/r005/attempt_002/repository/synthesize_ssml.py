import azure.cognitiveservices.speech as speechsdk


def synthesize_ssml(payload, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(payload['ssml']).get()
    
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure speech synthesis failed: {result.cancellation_details.error_details}")
    
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}