from google.cloud import texttospeech
import os

def synthesize_plain_text(text: str, output_filepath: str, voice_name: str = "en-US-Standard-A", language_code: str = "en-US"):
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file '{output_filepath}'")

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    synthesize_plain_text("Hello, this is a plain text synthesis example.", "output_plain.mp3")
