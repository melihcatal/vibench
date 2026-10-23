import os
from google.cloud import texttospeech

class ReviewerBriefAudioGenerator:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def generate_audio_brief(self, text: str, output_filepath: str) -> None:
        """
        Generates an audio file from the given text using Google Cloud Text-to-Speech API.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configure the voice.
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        # Configure the audio file type.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request.
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Write the response to the output file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
