import os
import base64
from typing import Dict, Any, Optional
from safety_client import SafetyClient


def reviewer_brief_audio(
    brief_text: str, voice_id: Optional[str] = None, language: str = "en"
) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers.

    Args:
        brief_text: The text to convert to speech
        voice_id: Optional specific voice ID to use
        language: Language code for the speech

    Returns:
        Dictionary with audio data and metadata
    """
    client = SafetyClient.get_client()

    # Use ElevenLabs for text-to-speech
    import requests

    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY not configured")

    # Default voice if not specified
    if not voice_id:
        # Use a professional-sounding voice for moderation briefs
        if language.startswith("en"):
            voice_id = (
                "21m00Tcm4TlvDq8ikWAM"  # Rachel - clear, professional female voice
            )
        elif language.startswith("es"):
            voice_id = "MF3mGyEYCl7XYWbV9V6O"  # Elli - Spanish female voice
        else:
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default to Rachel

    # Prepare request
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key,
    }

    data = {
        "text": brief_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True,
        },
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Get audio data
            audio_data = response.content

            # Encode to base64 for easier handling
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")

            # Get voice details
            voice_info_url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
            voice_response = requests.get(
                voice_info_url, headers={"xi-api-key": elevenlabs_api_key}
            )

            voice_info = {}
            if voice_response.status_code == 200:
                voice_data = voice_response.json()
                voice_info = {
                    "name": voice_data.get("name", "Unknown"),
                    "category": voice_data.get("category", "premade"),
                    "description": voice_data.get("description", ""),
                    "labels": voice_data.get("labels", {}),
                }

            return {
                "text": brief_text,
                "audio_data_base64": audio_base64,
                "audio_format": "mp3",
                "audio_size_bytes": len(audio_data),
                "voice_id": voice_id,
                "voice_info": voice_info,
                "language": language,
                "model": "eleven_monolingual_v1",
                "provider": "elevenlabs",
                "model_id": "eleven_monolingual_v1",
            }
        else:
            # Fallback to Google Text-to-Speech
            try:
                from google.cloud import texttospeech

                # Initialize client
                tts_client = texttospeech.TextToSpeechClient()

                # Set text input
                synthesis_input = texttospeech.SynthesisInput(text=brief_text)

                # Build voice request
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language,
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
                )

                # Select audio type
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )

                # Generate speech
                tts_response = tts_client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                audio_data = tts_response.audio_content
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")

                return {
                    "text": brief_text,
                    "audio_data_base64": audio_base64,
                    "audio_format": "mp3",
                    "audio_size_bytes": len(audio_data),
                    "voice_id": f"google-{language}",
                    "voice_info": {
                        "name": f"Google {language} voice",
                        "category": "google",
                        "language": language,
                    },
                    "language": language,
                    "model": "google-tts",
                    "provider": "google_cloud_tts",
                    "model_id": "google-text-to-speech",
                    "note": "Used Google TTS as fallback due to ElevenLabs error",
                }

            except Exception as google_error:
                return {
                    "text": brief_text,
                    "error": f"ElevenLabs TTS failed with status {response.status_code}, Google TTS fallback also failed: {str(google_error)}",
                    "provider": "none",
                    "model": "none",
                }

    except Exception as e:
        return {
            "text": brief_text,
            "error": f"TTS request failed: {str(e)}",
            "provider": "none",
            "model": "none",
        }
