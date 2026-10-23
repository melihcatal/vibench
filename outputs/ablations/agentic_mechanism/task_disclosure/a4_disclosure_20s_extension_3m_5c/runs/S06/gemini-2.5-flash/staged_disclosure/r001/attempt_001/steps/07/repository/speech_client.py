from google.cloud import texttospeech
import os

class SpeechClient:
    def __init__(self):
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # For local development, set this to the path of your service account key file.
        # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Text-to-Speech client might not authenticate correctly.")
        
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text: str, output_filename: str = "output.mp3", 
                          voice_name: str = "en-US-Standard-C", 
                          language_code: str = "en-US", 
                          audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3):
        """
        Synthesizes speech from the input text and saves it to an audio file.

        Args:
            text (str): The text to be synthesized.
            output_filename (str): The name of the file to save the audio to.
            voice_name (str): The name of the voice to use (e.g., "en-US-Standard-C").
            language_code (str): The language code for the voice (e.g., "en-US").
            audio_encoding (texttospeech.AudioEncoding): The encoding of the output audio.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example Usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # speech_client = SpeechClient()
    # speech_client.synthesize_speech(text="Hello, this is a test of the Google Cloud Text-to-Speech API.")
    pass
