from google.cloud import texttospeech

def generate_google_audio_briefing(text: str, output_filepath: str):
    """Generates a spoken briefing from text using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    # The concrete provider (Google Cloud Text-to-Speech API) is identified by the import
    # and the specific API endpoint and client usage.

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        
    return output_filepath
