from speech_client import create_speech_sdk, normalize_locale
from speech_models import TextToSpeechRequest, normalize_text


def synthesize_text(request: TextToSpeechRequest) -> bytes:
    speechsdk, speech_config = create_speech_sdk()
    speech_config.speech_synthesis_voice_name = request.voice or "en-US-JennyNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(normalize_text(request.text)).get()
    return result.audio_data
