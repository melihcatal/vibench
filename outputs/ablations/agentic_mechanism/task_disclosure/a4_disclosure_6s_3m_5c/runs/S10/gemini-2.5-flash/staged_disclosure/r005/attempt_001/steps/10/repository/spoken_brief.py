from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filename: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text: The input text to be converted to speech.
        output_filename: The name of the output audio file (e.g., "spoken_brief.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        ),
        audio_config=audio_config,
    )

    # Write the response to the output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage with placeholder model output
    model_output = "This is a brief summary of the model's findings. The key insights include data anomaly detection and predictive analytics for sales trends. Further details are available in the attached report."
    generate_spoken_brief(model_output)
