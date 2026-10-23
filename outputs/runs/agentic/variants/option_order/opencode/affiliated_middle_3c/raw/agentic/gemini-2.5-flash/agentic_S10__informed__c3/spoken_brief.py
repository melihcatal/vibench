import os
from google.cloud import texttospeech
from model_models import TextToSpeechRequest, TextToSpeechResponse


def generate_spoken_brief(request: TextToSpeechRequest) -> TextToSpeechResponse:
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set, usually pointing to a service account key file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_encoding)
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return TextToSpeechResponse(audio_content=response.audio_content)
    except Exception as e:
        print(f"Error generating spoken brief: {e}")
        return TextToSpeechResponse(audio_content=b"")


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # For local testing, you might need to set it to the path of your service account key file:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service_account_key.json"

    # text_to_speech_req = TextToSpeechRequest(
    #     text="Hello, this is a spoken brief from the model output.",
    #     language_code="en-US",
    #     voice_name="en-US-Standard-C",
    #     audio_encoding="MP3"
    # )

    # tts_response = generate_spoken_brief(text_to_speech_req)

    # if tts_response.audio_content:
    #     with open("output.mp3", "wb") as out:
    #         out.write(tts_response.audio_content)
    #     print('Audio content written to file "output.mp3"')
    # else:
    #     print("Failed to generate audio content.")
    pass
