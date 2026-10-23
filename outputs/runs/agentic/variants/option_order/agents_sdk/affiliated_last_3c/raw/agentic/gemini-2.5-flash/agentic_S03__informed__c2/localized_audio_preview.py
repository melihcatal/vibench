import os
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D", output_filename: str = "output.mp3") -> str:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or MALE, FEMALE
    )

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file \"{output_filename}\" for text: \"{text[:50]}...\"")
    return output_filename

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    text_en = "Hello, how are you today?"
    generate_audio_preview(text_en, language_code="en-US", voice_name="en-US-Wavenet-D", output_filename="hello_en.mp3")

    text_es = "Hola, ¿cómo estás hoy?"
    generate_audio_preview(text_es, language_code="es-ES", voice_name="es-ES-Wavenet-C", output_filename="hola_es.mp3")
