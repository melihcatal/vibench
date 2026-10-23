import os
from google.cloud import texttospeech

def retrieval_audio_brief(text_brief: str, output_filepath: str = "audio_brief.mp3", voice_name: str = "en-US-Wavenet-D") -> None:
    """Generates a spoken audio brief from text using Google Cloud Text-to-Speech.

    Args:
        text_brief: The text content for the audio brief.
        output_filepath: The path to save the generated audio file (e.g., "audio_brief.mp3").
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").
    """
    # Google Cloud Text-to-Speech client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    # Ensure your environment is authenticated (e.g., gcloud auth application-default login)
    # or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.

    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("NEUTRAL") or specific voice name.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name, # Example: en-US-Wavenet-D for a male voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # The response's audio_content is binary. Write it to a file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file: {output_filepath}")
    except Exception as e:
        print(f"Error generating audio brief with Google Cloud Text-to-Speech: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and valid, or default auth is configured.")

if __name__ == '__main__':
    # Example usage (ensure Google Cloud authentication is configured)
    # from dotenv import load_dotenv
    # load_dotenv()

    # brief_text = "Here is a summary of your retrieved search results. The top result discusses recent advancements in artificial intelligence. The second result covers ethical considerations of AI. And the third touches upon the impact of large language models."
    # retrieval_audio_brief(brief_text, "ai_brief.mp3")

    # brief_text_2 = "A quick news update. The local sports team won their championship game. And the weather forecast predicts sunshine for the weekend."
    # retrieval_audio_brief(brief_text_2, "news_brief.mp3", voice_name="en-GB-Wavenet-A")
    pass
