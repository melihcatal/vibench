import os
import json
import platform
import requests
from typing import Any, Dict

from model_client import ManagedModelClient


class ProviderConfig:
    """Configuration for Text-to-Speech (TTS) step.

    The class selects a concrete provider based on the presence of environment variables.
    At least one provider must be configured:
    - Google Cloud (GOOGLE_APPLICATION_CREDENTIALS + OS language settings)
    - Azure AI Speech (AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)
    - DashScope CosyVoice (DASHSCOPE_API_KEY)
    - ElevenLabs (ELEVENLABS_API_KEY)
    - Amazon Polly (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    - Watson (IBM_TTS_APIKEY, IBM_TTS_URL)
    """

    # ---------------------------------------------------------------
    # Provider identifiers (used only inside the file)
    # ---------------------------------------------------------------
    GOOGLE = "Google Cloud Text-to-Speech"
    AZURE = "Azure AI Speech TTS"
    DASHSCOPE = "DashScope CosyVoice"
    ELEVENLABS = "ElevenLabs"
    AMAZON = "Amazon Polly"
    WATSON = "Watson Text-to-Speech"

    # ---------------------------------------------------------------
    # Detect which provider is configured (mutual exclusive expectation)
    # ---------------------------------------------------------------
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        PROVIDER = GOOGLE
        GOOGLE_TTS = "https://texttospeech.googleapis.com/v1/text:synthesize"
        LANGUAGE_CODE = os.getenv("GOOGLE_TTS_LANGUAGE", "en-US")
        VOICE_NAME = os.getenv("GOOGLE_TTS_VOICE", "en-US-Wavenet-D")
    elif os.getenv("AZURE_SPEECH_KEY") and os.getenv("AZURE_SPEECH_REGION"):
        PROVIDER = AZURE
        PROVIDER = AZURE
        SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
        SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")
    elif os.getenv("DASHSCOPE_API_KEY"):
        PROVIDER = DASHSCOPE
        SPEECH_URL = "https://api.dashscope.ai/v1/tts"  # placeholder endpoint
    elif os.getenv("ELEVENLABS_API_KEY"):
        PROVIDER = ELEVENLABS
        SPEECH_URL = "https://api.elevenlabs.io/v1/text-to-speech"
    elif (
        os.getenv("AWS_ACCESS_KEY_ID")
        and os.getenv("AWS_SECRET_ACCESS_KEY")
        and os.getenv("AWS_REGION")
    ):
        PROVIDER = AMAZON
        POLLY_URL = f"https://{os.getenv('AWS_REGION')}.polly.amazonaws.com/v1/speech"
    elif os.getenv("IBM_TTS_APIKEY") and os.getenv("IBM_TTS_URL"):
        PROVIDER = WATSON
        SPEECH_URL = os.getenv("IBM_TTS_URL")
    else:
        raise RuntimeError(
            "No TTS provider configured. Set one of the required environment variables."
        )


def synthesize_speech(
    model: Any,  # Any model object; the content of `model` is the voice prompt
    text: str,
) -> Dict[str, Any]:
    """Generate spoken audio from `text` using the configured TTS provider.

    Returns a dict with keys: `audio_url`, `provider`, `metadata`.

    The function is synchronous and returns a URL to the generated audio file.
    """
    client = ManagedModelClient()
    payload = {"input": {"text": text}}
    # -------------------------------------------------------------------
    # Dispatch logic per provider
    # -------------------------------------------------------------------
    if ProviderConfig.PROVIDER == ProviderConfig.GOOGLE:
        # Google Cloud TTS requires language/voice config; payload is JSON
        headers = {
            "Authorization": f"Bearer {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}",
            "Content-Type": "application/json",
        }
        payload["input"]["voice"] = {
            "languageCode": ProviderConfig.LANGUAGE_CODE,
            "name": ProviderConfig.VOICE_NAME,
        }
        resp = requests.post(
            ProviderConfig.GOOGLE_TTS, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "audio_url": data["audioContent"],
            "provider": ProviderConfig.GOOGLE,
            "metadata": {
                "language": ProviderConfig.LANGUAGE_CODE,
                "voice": ProviderConfig.VOICE_NAME,
            },
        }
    elif ProviderConfig.PROVIDER == ProviderConfig.AZURE:
        # Azure Speech uses a multipart payload; request a SAS URL first (simplified)
        # For brevity we directly request synthesis via streaming endpoint
        headers = {
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
            "User-Agent": "AzureSpeechTTS",
        }
        # Note: Azure requires a separate SAS URL request; omitted here for brevity
        payload["input"]["format"] = "audio-24khz-96kbitrate-mono-mp3"
        resp = requests.post(
            f"https://{ProviderConfig.SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1",
            headers=headers,
            data=json.dumps(payload),
            auth=(ProviderConfig.SPEECH_KEY, ""),
        )
        resp.raise_for_status()
        # Azure returns the audio inline in the response body
        return {
            "audio_url": "data:audio/mpeg;base64," + resp.content.decode(),
            "provider": ProviderConfig.AZURE,
            "metadata": {"language": "en-US", "voice": "default"},
        }
    elif ProviderConfig.PROVIDER == ProviderConfig.DASHSCOPE:
        # DashScope CosyVoice (placeholder implementation)
        headers = {
            "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload["voice"] = "cosy-voice-default"
        resp = requests.post(
            ProviderConfig.SPEECH_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "audio_url": data["audioUrl"],
            "provider": ProviderConfig.DASHSCOPE,
            "metadata": {},
        }
    elif ProviderConfig.PROVIDER == ProviderConfig.ELEVENLABS:
        # ElevenLabs expects SSML or plain text + API key in header
        headers = {
            "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
            "Content-Type": "application/json",
        }
        payload["voice"] = "11voice-1"
        resp = requests.post(
            ProviderConfig.SPEECH_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "audio_url": data["audio_url"],
            "provider": ProviderConfig.ELEVENLABS,
            "metadata": {},
        }
    elif ProviderConfig.PROVIDER == ProviderConfig.AMAZON:
        # Amazon Polly request
        headers = {
            "x-amz-speech-version": "2020-01-01",
            "x-amz-custom-attributes": "text_type=plain",
        }
        headers["X-Amz-Date"] = client._sign_request(  # simplified placeholder
            request_method="POST",
            request_path="/v1/speech",
            headers={},
            body=json.dumps(payload),
        )
        payload["voice_id"] = "Joanna"
        resp = requests.post(
            ProviderConfig.POLLY_URL, json=payload, headers=headers, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "audio_url": data["audioStream"],
            "provider": ProviderConfig.AMAZON,
            "metadata": {"voice": "Joanna", "language": "en-US"},
        }
    elif ProviderConfig.PROVIDER == ProviderConfig.WATSON:
        # IBM Watson TTS request
        headers = {
            "X-Watson-Learning-Oriented": "1",
            "Content-Type": "application/json",
        }
        payload["accept"] = "audio/wav"
        resp = requests.post(
            ProviderConfig.SPEECH_URL,
            headers=headers,
            json=payload,
            auth=(ProviderConfig.APIKEY, ""),
            timeout=30,
        )
        resp.raise_for_status()
        audio_bytes = resp.content
        return {
            "audio_url": "data:audio/wav;base64," + audio_bytes.encode("base64"),
            "provider": ProviderConfig.WATSON,
            "metadata": {},
        }
    else:
        raise NotImplementedError(
            f"TTS provider {ProviderConfig.PROVIDER} not implemented"
        )


# ----------------------------------------------------------------------
# Example (disabled when package is imported)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     result = synthesize_speech(None, "Welcome to the managed model platform!")
#     print(result)
