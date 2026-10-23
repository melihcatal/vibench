import os
from google.cloud import texttospeech

def generate_audio_briefing(text_input, output_filename="briefing.mp3"):
    """
    Generates an audio briefing from the given text using Google Cloud Text-to-Speech.

    Args:
        text_input (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example voice, choose as appropriate
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure you have set up GOOGLE_APPLICATION_CREDENTIALS environment variable
    # pointing to your service account key file.
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    
    # Placeholder for platform output
    platform_output = "The system is currently operating at 95% capacity. All critical services are nominal. Minor network fluctuations detected in region East-1, but no service impact is anticipated."
    
    generate_audio_briefing(platform_output, "platform_briefing.mp3")
