import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import VoiceSelectionPayload

def select_voice(payload: VoiceSelectionPayload):
    speech_config = get_speech_config()
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    
    # Get all available voices
    result = speech_synthesizer.get_voices_async().get()
    
    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        voices_for_locale = []
        for voice in result.voices:
            if voice.locale == payload.locale:
                voices_for_locale.append({
                    "name": voice.name,
                    "display_name": voice.display_name,
                    "local_name": voice.local_name,
                    "gender": str(voice.gender).split('.')[-1],
                    "locale": voice.locale,
                    "sample_rate_hertz": voice.sample_rate_hertz,
                    "voice_type": str(voice.voice_type).split('.')[-1]
                })
        return {"voices": voices_for_locale}
    else:
        raise RuntimeError(f"Failed to retrieve voices: {result.reason}")
