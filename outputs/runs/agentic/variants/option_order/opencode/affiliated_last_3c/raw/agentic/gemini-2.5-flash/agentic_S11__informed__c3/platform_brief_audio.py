from google.cloud import texttospeech
import os


def generate_spoken_briefing(text: str, output_filepath: str, project_id: str):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice gender (optional)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    try:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file {output_filepath}")
        return True
    except IOError as e:
        print(f"Error writing audio file: {e}")
        return False


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if project_id:
        briefing_text = "This is a brief audio summary of the platform output. It contains important information and updates."
        output_file = "briefing.mp3"
        print(f"Generating spoken briefing to {output_file}...")
        success = generate_spoken_briefing(briefing_text, output_file, project_id)
        if success:
            print("Audio briefing generated successfully.")
        else:
            print("Failed to generate audio briefing.")
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID environment variable and ensure GOOGLE_APPLICATION_CREDENTIALS is set."
        )
