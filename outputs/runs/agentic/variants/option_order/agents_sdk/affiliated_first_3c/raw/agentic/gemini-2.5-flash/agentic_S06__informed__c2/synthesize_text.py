import os
from google.cloud import texttospeech

def synthesize_text_to_audio(text: str, output_filepath: str = "output.mp3"):
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to be returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-C"), audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    return output_filepath

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    synthesize_text_to_audio("Hello, this is a test of Google Cloud Text-to-Speech.")
