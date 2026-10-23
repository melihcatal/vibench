import os
from google.cloud import texttospeech

def generate_brief_audio(text: str, output_filepath: str = "output_audio.mp3") -> dict:
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {output_filepath}")
    
    return {"status": "success", "output_filepath": output_filepath}

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    brief_text = "This is a brief audio summary of the platform output. It can be used for quick updates or accessibility purposes."
    audio_info = generate_brief_audio(brief_text, "briefing_output.mp3")
    print(f"Audio generation result: {audio_info}")

    brief_text_two = "The latest report indicates a positive trend in user engagement this quarter."
    audio_info_two = generate_brief_audio(brief_text_two, "report_summary.mp3")
    print(f"Audio generation result: {audio_info_two}")
