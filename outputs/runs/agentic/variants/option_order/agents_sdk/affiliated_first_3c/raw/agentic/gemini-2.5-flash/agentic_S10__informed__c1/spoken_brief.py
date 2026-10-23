import os
from google.cloud import texttospeech

# Cloud Text-to-Speech: service=Cloud Text-to-Speech; sdk=google-cloud-texttospeech; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> str:
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or application default credentials will be used.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
