import os
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A", output_filename: str = "audio_preview.mp3"):
    """Generates a spoken audio preview of the given text using Google Cloud Text-to-Speech.

    Args:
        text: The text to be converted to speech.
        language_code: The language code for the synthesis (e.g., "en-US", "es-ES").
        voice_name: The name of the voice to use (e.g., "en-US-Standard-A").
        output_filename: The name of the file to save the audio to.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'''Audio content written to file "{output_filename}"''')

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    
    # generate_audio_preview("Hello, this is a test of the audio preview.", "en-US", "en-US-Wavenet-D", "test_audio.mp3")
    pass
