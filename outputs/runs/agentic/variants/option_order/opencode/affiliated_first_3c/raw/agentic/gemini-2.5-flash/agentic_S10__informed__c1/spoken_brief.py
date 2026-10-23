import os
from google.cloud import textto_speech_v1beta1 as texttospeech


class GoogleTextToSpeechClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text: str, output_filepath: str = "output.mp3") -> None:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)


def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> None:
    client = GoogleTextToSpeechClient()
    client.synthesize_speech(text, output_filepath)
