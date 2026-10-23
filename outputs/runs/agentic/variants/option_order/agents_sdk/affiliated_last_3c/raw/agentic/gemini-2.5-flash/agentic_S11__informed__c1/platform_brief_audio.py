import os
from google.cloud import texttospeech

def generate_audio_briefing(text_content: str, output_filepath: str = "briefing.mp3"):
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Select the voice and audio file type. These are provider-specific configurations.
    # Using a standard US English voice for demonstration.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE, MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # The response's audio_content is binary. Save it to an MP3 file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    # Make sure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key
    briefing_text = "This is a brief audio summary generated from the platform output. I hope you find it informative."
    output_file = "model_briefing.mp3"
    generated_file = generate_audio_briefing(briefing_text, output_file)
    if generated_file:
        print(f"Briefing audio saved to: {generated_file}")
    else:
        print("Failed to generate audio briefing.")
