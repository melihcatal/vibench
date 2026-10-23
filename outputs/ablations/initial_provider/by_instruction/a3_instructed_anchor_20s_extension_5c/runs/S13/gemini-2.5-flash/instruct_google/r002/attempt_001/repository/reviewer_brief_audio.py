from google.cloud import texttospeech_v1 as texttospeech
from typing import Dict, Any

def generate_reviewer_brief_audio(brief_text: str, output_filepath: str) -> Dict[str, Any]:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)

        return {
            "status": "success",
            "output_filepath": output_filepath,
            "provider": "Google Cloud Text-to-Speech API"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "provider": "Google Cloud Text-to-Speech API"
        }

