from google.cloud import texttospeech
import os

def generate_audio_from_text(text: str, output_filename: str, project_id: str):
    """Generates spoken briefings from text using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (e.g., "neutral")
    # Provider-identifying signal: google.cloud.texttospeech.TextToSpeechClient and specific voice names.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-J", # A specific standard voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Save it to an MP3 file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filename}" in project {project_id}')

if __name__ == '__main__':
    import os
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

    briefing_text = (
        "Good morning. Here is your daily briefing. "
        "The stock market saw a slight increase yesterday, and weather forecasts predict sunny skies. "
        "Remember to stay hydrated and have a productive day."
    )
    output_file = "daily_briefing.mp3"

    generate_audio_from_text(briefing_text, output_file, project_id)
    print(f"Generated audio briefing saved as {output_file}")

    briefing_text_2 = (
        "This is a critical alert. "
        "Please review the latest security patch immediately. "
        "Further details have been sent to your registered email address."
    )
    output_file_2 = "critical_alert.mp3"
    generate_audio_from_text(briefing_text_2, output_file_2, project_id)
    print(f"Generated audio briefing saved as {output_file_2}")
