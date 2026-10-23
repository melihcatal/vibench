import os
from google.cloud import texttospeech
from typing import Optional


def generate_speech_google_cloud(
    text: str, output_filepath: str, project_id: Optional[str] = None
):
    """
    Generates spoken audio from text using Google Cloud Text-to-Speech.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # If project_id is not provided, the client will try to infer it from the environment or credentials.
    client = texttospeech.TextToSpeechClient(project=project_id)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-A",  # You can choose other voices, e.g., "en-US-Wavenet-F"
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the audio file type
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


if __name__ == "__main__":
    # For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    google_cloud_project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # Optional, client can infer

    test_text = (
        "This is a brief audio message generated using Google Cloud Text-to-Speech."
    )
    output_audio_file = "briefing.mp3"

    print(f"Generating speech for: '{test_text}'")
    try:
        generate_speech_google_cloud(
            test_text, output_audio_file, project_id=google_cloud_project_id
        )
    except Exception as e:
        print(f"Error generating speech: {e}")
