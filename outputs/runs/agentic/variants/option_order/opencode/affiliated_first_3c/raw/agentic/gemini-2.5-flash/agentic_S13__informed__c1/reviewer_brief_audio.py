from google.cloud import texttospeech
import os


def reviewer_brief_audio(brief_text, output_filename="reviewer_brief.mp3"):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    # or authentication configured otherwise.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    return f"Audio content written to file '{output_filename}'"


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set)
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key file."
        )
    else:
        brief = "Reviewer brief: User reported a comment with high toxicity. The comment contained insults and profanity. Please review for policy violations."
        output_file = "moderation_brief.mp3"
        result = reviewer_brief_audio(brief, output_file)
        print(result)
        print(f"You can now play the audio file: {output_file}")
