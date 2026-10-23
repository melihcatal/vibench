from google.cloud import texttospeech
from typing import List

def generate_audio_brief(project_id: str, text_brief: str, output_filepath: str = "audio_brief.mp3", language_code: str = "en-US", voice_name: str = "en-US-Standard-A") -> str:
    """Generates a spoken audio brief from text using Google Cloud Text-to-Speech API.

    Args:
        project_id: Your Google Cloud project ID.
        text_brief: The text content for the audio brief.
        output_filepath: The path to save the generated audio file (default: "audio_brief.mp3").
        language_code: The language code for the voice (e.g., "en-US").
        voice_name: The name of the voice to use (e.g., "en-US-Standard-A").

    Returns:
        The path to the saved audio file.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient(client_options={"quota_project_id": project_id})

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Build the voice request, select the language code and a voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        # print(f'Audio content written to file "{output_filepath}"')

    return output_filepath

if __name__ == '__main__':
    # Example usage:
    # # Replace with your actual project_id
    # PROJECT_ID = "your-project-id"

    # search_results_text = (
    #     "According to the retrieved documents, machine learning is a subset of artificial intelligence "
    #     "that focuses on systems learning from data to identify patterns and make decisions with minimal human intervention. "
    #     "Key applications include natural language processing and image recognition."
    # )

    # output_file = generate_audio_brief(
    #     project_id=PROJECT_ID,
    #     text_brief=search_results_text,
    #     output_filepath="search_brief.mp3"
    # )
    # print(f"Generated audio brief: {output_file}")
    pass
