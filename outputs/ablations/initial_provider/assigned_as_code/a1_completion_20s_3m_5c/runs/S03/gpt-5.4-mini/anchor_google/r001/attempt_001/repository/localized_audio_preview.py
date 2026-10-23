from google.cloud import texttospeech

from translation_models import normalize_payload


def localized_audio_preview(payload, config=None):
    config = config or {}
    payload = normalize_payload(payload)
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(language_code=payload["target_language"])
    synthesis_input = texttospeech.SynthesisInput(text=payload["text"])
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return {
        "audio_content": response.audio_content,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
