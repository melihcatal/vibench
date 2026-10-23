import os
import base64
from typing import Dict, Any, Optional
from google.cloud import texttospeech


def text_to_speech(
    text: str,
    voice_name: str = "en-US-Neural2-J",
    language_code: str = "en-US",
    audio_format: str = "MP3",
) -> Dict[str, Any]:
    """Generate spoken briefings from platform outputs using Google Cloud Text-to-Speech."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return {
            "text": text[:100],
            "audio_data": None,
            "error": "GOOGLE_CLOUD_PROJECT environment variable not set",
            "voice": voice_name,
            "format": audio_format,
        }

    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=get_audio_encoding(audio_format),
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0,
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        audio_content = response.audio_content
        audio_base64 = base64.b64encode(audio_content).decode("utf-8")

        return {
            "text": text[:500],  # Truncate for display
            "audio_data": audio_base64,
            "audio_size_bytes": len(audio_content),
            "voice": voice_name,
            "language_code": language_code,
            "audio_format": audio_format,
            "project_id": project_id,
            "tts_provider": "google-cloud-text-to-speech",
        }

    except Exception as e:
        return {
            "text": text[:100],
            "audio_data": None,
            "error": str(e),
            "voice": voice_name,
            "format": audio_format,
            "tts_provider": "google-cloud-text-to-speech",
        }


def get_audio_encoding(format_str: str) -> texttospeech.AudioEncoding:
    """Convert format string to AudioEncoding enum."""
    format_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        "MULAW": texttospeech.AudioEncoding.MULAW,
        "ALAW": texttospeech.AudioEncoding.ALAW,
    }
    return format_map.get(format_str.upper(), texttospeech.AudioEncoding.MP3)


def list_available_voices(language_code: str = "en-US") -> Dict[str, Any]:
    """List available voices for a language."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return {
            "language_code": language_code,
            "voices": [],
            "error": "GOOGLE_CLOUD_PROJECT not set",
        }

    try:
        client = texttospeech.TextToSpeechClient()

        voices_response = client.list_voices(language_code=language_code)

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
            "language_code": language_code,
            "voices": voices,
            "total_voices": len(voices),
            "project_id": project_id,
        }

    except Exception as e:
        return {
            "language_code": language_code,
            "voices": [],
            "error": str(e),
            "project_id": project_id,
        }


def generate_briefing_from_model_output(
    model_output: Dict[str, Any], voice_name: str = "en-US-Neural2-J"
) -> Dict[str, Any]:
    """Generate audio briefing from model output."""
    text = ""

    if "content" in model_output:
        text = model_output["content"]
    elif "text" in model_output:
        text = model_output["text"]
    elif "response" in model_output:
        text = model_output["response"]
    else:
        text = str(model_output)

    briefing_text = f"Model briefing: {text}"

    if len(briefing_text) > 5000:
        briefing_text = briefing_text[:5000] + "... [truncated]"

    return text_to_speech(briefing_text, voice_name)


def batch_text_to_speech(
    texts: List[str], voice_name: str = "en-US-Neural2-J", language_code: str = "en-US"
) -> List[Dict[str, Any]]:
    """Convert multiple texts to speech."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return [
            {
                "text": text[:100],
                "audio_data": None,
                "error": "GOOGLE_CLOUD_PROJECT not set",
                "text_index": i,
                "voice": voice_name,
            }
            for i, text in enumerate(texts)
        ]

    try:
        client = texttospeech.TextToSpeechClient()

        results = []
        for i, text in enumerate(texts):
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code, name=voice_name
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.0
            )

            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")

            results.append(
                {
                    "text": text[:500],
                    "audio_data": audio_base64,
                    "audio_size_bytes": len(response.audio_content),
                    "text_index": i,
                    "voice": voice_name,
                    "language_code": language_code,
                    "tts_provider": "google-cloud-text-to-speech",
                }
            )

        return results

    except Exception as e:
        return [
            {
                "text": text[:100],
                "audio_data": None,
                "error": str(e),
                "text_index": i,
                "voice": voice_name,
            }
            for i, text in enumerate(texts)
        ]


def get_recommended_voices() -> Dict[str, List[str]]:
    """Get recommended voice configurations."""
    return {
        "english": [
            "en-US-Neural2-J",  # Male, standard
            "en-US-Neural2-F",  # Female, standard
            "en-US-Studio-O",  # Male, studio quality
            "en-US-Studio-M",  # Female, studio quality
            "en-US-Wavenet-D",  # Male, wavenet
            "en-US-Wavenet-C",  # Female, wavenet
        ],
        "spanish": [
            "es-US-Neural2-A",  # Female, US Spanish
            "es-US-Neural2-B",  # Male, US Spanish
            "es-ES-Neural2-F",  # Female, Spain Spanish
            "es-ES-Neural2-D",  # Male, Spain Spanish
        ],
        "multilingual": [
            "en-US-Neural2-J",  # English
            "es-US-Neural2-A",  # Spanish
            "fr-FR-Neural2-A",  # French
            "de-DE-Neural2-F",  # German
            "ja-JP-Neural2-B",  # Japanese
        ],
    }


if __name__ == "__main__":
    test_text = "The model analysis indicates a 75% probability of market growth in the technology sector. Key factors include increased AI adoption and cloud computing expansion."

    # Test text-to-speech
    audio_result = text_to_speech(test_text)
    print(f"Audio generated: {audio_result['audio_size_bytes']} bytes")
    print(f"Voice: {audio_result['voice']}")

    # Test voice listing
    voices = list_available_voices("en-US")
    print(f"Available English voices: {voices.get('total_voices', 0)}")

    # Test model output briefing
    model_output = {
        "content": "Based on the data analysis, we recommend investing in renewable energy stocks.",
        "model_deployment": "text-bison",
        "confidence": 0.85,
    }

    briefing = generate_briefing_from_model_output(model_output)
    print(f"Briefing audio size: {briefing.get('audio_size_bytes', 0)} bytes")
