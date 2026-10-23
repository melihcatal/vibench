import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import normalize_voice_payload


def select_voice(payload, config=None):
    payload = normalize_voice_payload(payload)
    speech_config = load_speech_config(config)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    voices = synthesizer.get_voices_async(payload.get('locale', 'en-US')).get()
    if voices.reason != speechsdk.ResultReason.VoicesListRetrieved:
        raise RuntimeError('Azure voice listing failed')
    selected = None
    for voice in voices.voices:
        if payload.get('voice') and voice.short_name == payload['voice']:
            selected = voice
            break
        if not payload.get('voice') and voice.locale == payload.get('locale', 'en-US'):
            selected = voice
            break
    if selected is None and voices.voices:
        selected = voices.voices[0]
    if selected is None:
        raise RuntimeError('No Azure voices found')
    return {'name': selected.short_name, 'locale': selected.locale}
