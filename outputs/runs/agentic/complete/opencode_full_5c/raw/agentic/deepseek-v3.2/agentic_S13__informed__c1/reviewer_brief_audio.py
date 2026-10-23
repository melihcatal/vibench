import os
from typing import Dict, Any
import base64


def reviewer_brief_audio(
    brief_text: str, output_file: str = "brief_audio.mp3"
) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    from google.cloud import texttospeech

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = texttospeech.TextToSpeechClient()

    try:
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=brief_text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.0, pitch=0.0
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Write the response to the output file
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        # Get file size
        file_size = os.path.getsize(output_file)

        # Encode audio for potential API return
        with open(output_file, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        return {
            "text": brief_text,
            "audio_file": output_file,
            "file_size": file_size,
            "audio_format": "mp3",
            "voice": "en-US-Neural2-J",
            "provider": "google_cloud_tts",
            "service": "google.cloud.texttospeech",
            "audio_base64": audio_base64[:100] + "..."
            if len(audio_base64) > 100
            else audio_base64,
        }

    except Exception as e:
        return {
            "text": brief_text,
            "audio_file": None,
            "error": str(e),
            "provider": "google_cloud_tts",
        }
