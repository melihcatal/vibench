from google.cloud import texttospeech
import os

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> str:
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    Expects GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Google Cloud Text-to-Speech might not authenticate correctly.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filepath}'")
    
    return output_filepath
