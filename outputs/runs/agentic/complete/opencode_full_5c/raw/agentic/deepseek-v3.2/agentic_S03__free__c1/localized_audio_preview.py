import os
from typing import Optional
from dataclasses import dataclass
from translation_client import get_translation_client


@dataclass
class AudioPreviewResult:
    """Result of audio preview generation."""

    audio_content: bytes
    audio_format: str
    language_code: str
    voice_name: str
    audio_uri: Optional[str] = None


def localized_audio_preview(
    text: str, language_code: str = "en-US", voice_name: Optional[str] = None
) -> AudioPreviewResult:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech API."""
    try:
        from google.cloud import texttospeech

        client = texttospeech.TextToSpeechClient()

        if voice_name is None:
            if language_code.startswith("en"):
                voice_name = "en-US-Neural2-J"
            elif language_code.startswith("es"):
                voice_name = "es-US-Neural2-B"
            elif language_code.startswith("fr"):
                voice_name = "fr-FR-Neural2-A"
            elif language_code.startswith("de"):
                voice_name = "de-DE-Neural2-F"
            elif language_code.startswith("ja"):
                voice_name = "ja-JP-Neural2-B"
            else:
                voice_name = "en-US-Neural2-J"

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0,
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return AudioPreviewResult(
            audio_content=response.audio_content,
            audio_format="mp3",
            language_code=language_code,
            voice_name=voice_name,
        )

    except Exception as e:
        print(f"Audio preview generation error: {e}")

        import io
        from gtts import gTTS

        try:
            tts = gTTS(text=text, lang=language_code[:2], slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            return AudioPreviewResult(
                audio_content=audio_buffer.read(),
                audio_format="mp3",
                language_code=language_code,
                voice_name="gTTS-default",
            )
        except Exception as gtts_error:
            print(f"gTTS fallback error: {gtts_error}")

            return AudioPreviewResult(
                audio_content=b"",
                audio_format="mp3",
                language_code=language_code,
                voice_name="error",
                audio_uri=None,
            )
