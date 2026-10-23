import azure.cognitiveservices.speech as speechsdk

from speech_client import configure_output_format, configure_voice, load_speech_config


def synthesize_ssml(payload, config=None):
    config = config or {}
    speech_config = configure_output_format(configure_voice(load_speech_config(config), config.get('voice', 'en-US-JennyNeural')), config.get('content_type', 'audio/mpeg'))
    result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_ssml_async(payload['ssml']).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure speech synthesis failed')
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
