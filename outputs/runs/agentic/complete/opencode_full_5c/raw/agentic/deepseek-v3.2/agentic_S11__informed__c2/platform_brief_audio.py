import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any, Optional
import base64


def generate_speech_with_watson(
    text: str, voice: str = "en-US_AllisonV3Voice", accept: str = "audio/mp3"
) -> Dict[str, Any]:
    """
    Generate spoken briefings from platform outputs using Watson Text to Speech.
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    service_url = os.getenv("IBM_TTS_URL")

    if not api_key or not service_url:
        raise ValueError(
            "IBM Watson TTS API key and URL must be set in environment variables"
        )

    try:
        authenticator = IAMAuthenticator(api_key)
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(service_url)

        response = text_to_speech.synthesize(
            text=text, voice=voice, accept=accept
        ).get_result()

        audio_content = response.content

        return {
            "audio_data": base64.b64encode(audio_content).decode("utf-8"),
            "audio_format": accept,
            "voice": voice,
            "text_length": len(text),
            "provider": "IBM Watson Text to Speech",
        }

    except Exception as e:
        return {
            "audio_data": "",
            "error": f"Watson TTS error: {str(e)}",
            "voice": voice,
            "provider": "IBM Watson Text to Speech",
        }


def create_briefing_audio(
    text: str, briefing_type: str = "summary", language: str = "en-US"
) -> Dict[str, Any]:
    """
    Create a spoken briefing from text with appropriate voice selection.
    """
    voice_map = {
        "en-US": {
            "standard": "en-US_AllisonV3Voice",
            "expressive": "en-US_EmmaExpressive",
            "news": "en-US_MichaelV3Voice",
        },
        "en-GB": {
            "standard": "en-GB_CharlotteV3Voice",
            "expressive": "en-GB_JamesV3Voice",
        },
        "de-DE": {
            "standard": "de-DE_BirgitV3Voice",
            "expressive": "de-DE_DieterV3Voice",
        },
        "fr-FR": {
            "standard": "fr-FR_ReneeV3Voice",
            "expressive": "fr-FR_NicolasV3Voice",
        },
        "es-ES": {
            "standard": "es-ES_EnriqueV3Voice",
            "expressive": "es-ES_LauraV3Voice",
        },
    }

    base_lang = (
        language.split("-")[0] + "-" + language.split("-")[1]
        if "-" in language
        else language
    )

    if base_lang in voice_map:
        voice_options = voice_map[base_lang]
        voice = voice_options.get(briefing_type, voice_options["standard"])
    else:
        voice = "en-US_AllisonV3Voice"

    briefing_text = format_briefing_text(text, briefing_type)

    return generate_speech_with_watson(
        text=briefing_text, voice=voice, accept="audio/mp3"
    )


def format_briefing_text(text: str, briefing_type: str) -> str:
    """
    Format text for briefing audio generation.
    """
    if briefing_type == "summary":
        if len(text) > 500:
            summary = text[:497] + "..."
        else:
            summary = text
        return f"Here is your briefing summary: {summary}"

    elif briefing_type == "news":
        return f"News update: {text}"

    elif briefing_type == "alert":
        return f"Alert: {text}"

    else:
        return text


def save_audio_to_file(
    audio_data: Dict[str, Any], filename: str = "briefing.mp3"
) -> bool:
    """
    Save base64 encoded audio data to file.
    """
    try:
        if "audio_data" not in audio_data or not audio_data["audio_data"]:
            return False

        audio_bytes = base64.b64decode(audio_data["audio_data"])

        with open(filename, "wb") as f:
            f.write(audio_bytes)

        return True

    except Exception as e:
        print(f"Error saving audio file: {e}")
        return False
