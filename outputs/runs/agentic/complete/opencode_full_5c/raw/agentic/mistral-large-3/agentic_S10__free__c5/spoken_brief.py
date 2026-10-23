from typing import Optional, Dict, Any
import os
import io
import base64
from google.cloud import texttospeech
from google.oauth2 import service_account


def generate_spoken_brief(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Wavenet-D",
    api_key: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> bytes:
    """
    Generate a spoken brief from the model output using Google Cloud Text-to-Speech API.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
    else:
        credentials = service_account.Credentials.from_service_account_info(
            {
                "type": os.getenv("GOOGLE_TYPE"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv(
                    "GOOGLE_AUTH_PROVIDER_CERT_URL"
                ),
                "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
            }
        )

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
