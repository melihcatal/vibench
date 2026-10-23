from google.cloud import texttospeech
import os
from typing import List

def generate_spoken_brief_from_retrieval(brief_text: str, output_filepath: str = "retrieval_brief.mp3") -> str:
    """Generates an audio brief from retrieved search results text using Google Cloud Text-to-Speech.

    Args:
        brief_text: The concatenated or summarized text from retrieved search results.
        output_filepath: The path where the generated audio file (MP3) will be saved.

    Returns:
        The path to the generated audio file.
    """
    # Google Cloud Text-to-Speech client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods if available in the environment.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the language and SSML Voice Type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filepath}"' )
    return output_filepath

if __name__ == '__main__':
    sample_brief = (
        "Here is a brief summary of your retrieved search results. "
        "The top result suggests visiting national parks in summer. "
        "Another relevant document highlights hiking and camping as popular warm-weather activities. "
        "Consider these options for your next summer vacation planning." 
    )
    output_file = "retrieval_brief_example.mp3"

    print("Generating audio brief...")
    try:
        generated_file = generate_spoken_brief_from_retrieval(sample_brief, output_file)
        print(f"Audio brief saved to: {generated_file}")
        print("To play the audio, use a media player or a library like `playsound`.")
    except Exception as e:
        print(f"Error generating audio brief: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS are configured (e.g., via `gcloud auth application-default login`).")
