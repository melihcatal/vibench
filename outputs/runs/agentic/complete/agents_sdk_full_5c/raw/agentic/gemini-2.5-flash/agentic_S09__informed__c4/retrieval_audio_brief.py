import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    """
    Generates a spoken audio brief from retrieved search results text using Google Cloud Text-to-Speech.
    The audio is saved to a specified MP3 file.
    """
    # Google Cloud Text-to-Speech automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods if set up.
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice (e.g., US English, Wavenet voice for high quality)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-A", # Or another preferred Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want (e.g., MP3)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    
    return output_filepath

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS are set up, e.g., via a service account JSON file
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    brief_text = "Here is a brief summary of the top search results. The first result discusses the best practices for cloud security. The second covers recent advancements in artificial intelligence. And the third highlights new sustainable energy solutions."
    output_file = "search_brief.mp3"

    try:
        generated_file = generate_audio_brief(brief_text, output_file)
        print(f"Successfully generated audio brief at: {generated_file}")
    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS are correctly configured for Google Cloud Text-to-Speech.")
