import os
import base64
from typing import Dict, Any, Optional
from translation_models import TranslationResponse


def generate_spoken_preview(
    translated_text: str, language_code: str = "es", voice_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate spoken previews of translated copy using Google Cloud Text-to-Speech API.

    Args:
        translated_text: Translated text to convert to speech
        language_code: Language code for speech synthesis
        voice_name: Optional specific voice name (e.g., "es-US-Standard-A")

    Returns:
        Dictionary with audio data and metadata
    """
    try:
        # Import Google Cloud Text-to-Speech
        from google.cloud import texttospeech

        # Initialize client
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=translated_text)

        # Build the voice request
        if voice_name:
            voice = texttospeech.VoiceSelectionParams(
                name=voice_name, language_code=language_code
            )
        else:
            # Auto-select voice based on language
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0,
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Encode audio content to base64 for easy transmission
        audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")

        # Get voice details
        voices_response = client.list_voices(language_code=language_code)
        available_voices = [
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
            for voice in voices_response.voices
        ]

        # Create result metadata
        result = {
            "text": translated_text,
            "language_code": language_code,
            "voice_used": voice.name if voice_name else "auto-selected",
            "audio_format": "MP3",
            "audio_size_bytes": len(response.audio_content),
            "audio_base64": audio_base64,
            "available_voices": available_voices[:5],  # First 5 voices
            "synthesis_parameters": {
                "speaking_rate": 1.0,
                "pitch": 0.0,
                "volume_gain_db": 0.0,
            },
        }

        return result

    except Exception as e:
        raise Exception(f"Audio preview generation failed: {str(e)}")


def get_available_voices(language_code: str = None) -> Dict[str, Any]:
    """
    Get available voices for text-to-speech synthesis.

    Args:
        language_code: Optional language code filter

    Returns:
        Dictionary with available voices
    """
    try:
        from google.cloud import texttospeech

        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        client = texttospeech.TextToSpeechClient()

        if language_code:
            voices_response = client.list_voices(language_code=language_code)
        else:
            voices_response = client.list_voices()

        voices = []
        for voice in voices_response.voices:
            voice_info = {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
            voices.append(voice_info)

        return {
            "total_voices": len(voices),
            "voices": voices,
            "filter_language": language_code,
        }

    except Exception as e:
        raise Exception(f"Failed to get available voices: {str(e)}")


def save_audio_preview(audio_data: Dict[str, Any], output_path: str) -> str:
    """
    Save audio preview to file.

    Args:
        audio_data: Audio data from generate_spoken_preview
        output_path: Path to save audio file

    Returns:
        Path to saved file
    """
    try:
        audio_base64 = audio_data.get("audio_base64")
        if not audio_base64:
            raise ValueError("No audio data in provided dictionary")

        # Decode base64 audio
        audio_content = base64.b64decode(audio_base64)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Write audio file
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_content)

        return output_path

    except Exception as e:
        raise Exception(f"Failed to save audio preview: {str(e)}")
