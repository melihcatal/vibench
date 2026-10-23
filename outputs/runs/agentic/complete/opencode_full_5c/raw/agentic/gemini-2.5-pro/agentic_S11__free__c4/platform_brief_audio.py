from google.cloud import texttospeech
from model_client import get_google_cloud_project


def generate_audio_briefing(text: str, output_file: str = "briefing.mp3") -> None:
    """
    Generates a spoken briefing from platform output using Google Cloud Text-to-Speech.

    Args:
        text: The text to synthesize into speech.
        output_file: The path to save the output audio file.
    """
    project_id = get_google_cloud_project()
    if not project_id:
        # The client can sometimes infer the project, but we check for clarity.
        print("Warning: GOOGLE_CLOUD_PROJECT not set, relying on client inference.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Use a provider-specific voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_file}'")


if __name__ == "__main__":
    try:
        from invoke_platform_model import invoke_model

        # 1. Get a brief text from the platform model
        briefing_text_response = invoke_model(
            "Summarize the importance of renewable energy in two sentences."
        )
        print(f"Text to be synthesized: {briefing_text_response.text}")

        # 2. Generate the audio file
        generate_audio_briefing(briefing_text_response.text)

    except (ValueError, ImportError) as e:
        print(f"Error generating audio briefing: {e}")
