import os
from google.cloud import texttospeech


def generate_audio_brief(text_brief: str, output_file: str = "briefing.mp3") -> str:
    """
    Generates a spoken audio brief from retrieved search results text.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "gcp_credentials.json"
    )
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')

    return output_file


if __name__ == "__main__":
    retrieved_text = "Based on your query, the top result is about the Eiffel Tower, a famous landmark in Paris, France. It was completed in 1889 and is a popular tourist destination."
    generate_audio_brief(retrieved_text)
