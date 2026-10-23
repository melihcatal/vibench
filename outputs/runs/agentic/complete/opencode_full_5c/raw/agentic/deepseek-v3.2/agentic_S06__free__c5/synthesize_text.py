from google.cloud import texttospeech
import speech_client


def synthesize_text(text, language_code="en-US", voice_name=None):
    """Synthesize plain text to audio byte stream using Google Cloud TTS."""
    client = speech_client.get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name if voice_name else f"{language_code}-Standard-A",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
