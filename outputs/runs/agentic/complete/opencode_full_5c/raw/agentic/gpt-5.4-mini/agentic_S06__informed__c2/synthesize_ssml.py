from speech_client import create_speech_sdk, normalize_locale
from speech_models import TextToSpeechRequest, normalize_ssml


def synthesize_ssml(
    request: TextToSpeechRequest, rate: str = "0%", pitch: str = "0%"
) -> bytes:
    speechsdk, speech_config = create_speech_sdk()
    voice = request.voice or "en-US-JennyNeural"
    ssml = normalize_ssml(request.text, voice, normalize_locale(request.locale))
    ssml = ssml.replace(
        f">{request.text.strip()}<",
        f'><prosody rate="{rate}" pitch="{pitch}">{request.text.strip()}</prosody><',
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    result = synthesizer.speak_ssml_async(ssml).get()
    return result.audio_data
