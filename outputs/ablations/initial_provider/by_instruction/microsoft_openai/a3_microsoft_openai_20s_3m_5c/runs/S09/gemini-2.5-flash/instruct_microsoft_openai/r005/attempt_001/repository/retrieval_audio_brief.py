import os
from typing import List, Dict, Any
from google.cloud import texttospeech

def generate_retrieval_audio_brief(text_brief: str, output_filepath: str = "audio_brief.mp3") -> Dict[str, str]:
    """Generates a spoken audio brief from retrieved search results text using Google Cloud Text-to-Speech API.

    Args:
        text_brief: The text content of the brief to convert to speech.
        output_filepath: The path to save the generated audio file (e.g., "audio_brief.mp3").

    Returns:
        A dictionary indicating the status and the path of the generated audio file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Or FEMALE, MALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary. Write it to a file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return {"status": "success", "audio_filepath": output_filepath, "message": "Audio brief generated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

