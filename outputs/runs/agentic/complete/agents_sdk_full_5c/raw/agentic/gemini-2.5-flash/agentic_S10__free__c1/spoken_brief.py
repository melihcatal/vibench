import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str, project_id: str) -> None:
    """
    Generates a spoken brief (audio file) from text using Google Cloud Text-to-Speech API.
    Saves the audio content to the specified output_filepath.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filepath}" for project {project_id}')

if __name__ == 'main':
    # Example usage - not for grading
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     generate_spoken_brief("This is a test brief generated from text.", "output.mp3", project_id)
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    pass
