from google.cloud import texttospeech
from typing import Dict, Any, Optional

def platform_brief_audio(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A") -> Dict[str, Any]:
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech API."
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code and a SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,  # e.g., 'en-US-Wavenet-D' or 'en-US-Standard-A'
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}" ')
    
    return {
        "text": text,
        "output_filepath": output_filepath,
        "audio_length_bytes": len(response.audio_content)
    }
