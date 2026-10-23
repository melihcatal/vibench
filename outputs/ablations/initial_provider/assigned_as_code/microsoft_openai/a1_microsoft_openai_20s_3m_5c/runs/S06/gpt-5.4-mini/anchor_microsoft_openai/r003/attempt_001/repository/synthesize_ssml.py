import azure.cognitiveservices.speech as speechsdk

from speech_client import load_tts_config


def synthesize_ssml(payload, config=None):
    config = load_tts_config(config)
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_synthesis_voice_name = payload.get('voice') or config['voice']
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    audio = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_ssml_async(payload['ssml']).get()
    if audio.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure SSML synthesis failed')
    return {'audio_bytes': audio.audio_data, 'content_type': 'audio/mpeg'}
