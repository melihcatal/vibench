from typing import Dict, Any, Optional
import requests
import base64
from .model_client import get_model_client_config
from .model_models import ChatResponse


def platform_brief_audio(
    response: ChatResponse,
    voice_name: str = "en-US-JennyNeural",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generates spoken briefings from Azure AI Inference model output using Azure Text-to-Speech.
    """
    config = get_model_client_config()
    api_key = api_key or config.get("AZURE_SPEECH_KEY")
    region = config.get("AZURE_SPEECH_REGION", "eastus")

    if not api_key:
        raise ValueError("Missing required configuration for Azure Speech Service.")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
    }

    ssml = f"""<speak version='1.0' xml:lang='en-US'>
        <voice name='{voice_name}'>
            {response.content}
        </voice>
    </speak>"""

    speech_response = requests.post(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        headers=headers,
        data=ssml.encode("utf-8"),
    )
    speech_response.raise_for_status()

    audio_content = speech_response.content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    return {
        "audio_content": audio_base64,
        "format": "mp3",
        "voice": voice_name,
    }
