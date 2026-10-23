import os
from typing import Union
import openai

class TTSClient:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15", # Or the appropriate API version for TTS
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        # This should be your deployed TTS model name, if applicable, or default OpenAI model
        self.tts_model_name = os.getenv("AZURE_OPENAI_TTS_MODEL_NAME", "tts-1")

def generate_audio_preview(text: str, voice: str = "alloy", output_filepath: str = "audio_preview.mp3") -> str:
    """
    Generates a spoken preview of translated copy using OpenAI's Text-to-Speech API.

    Args:
        text: The text to convert to speech.
        voice: The voice to use for the audio. Options: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.
        output_filepath: The path to save the generated audio file.

    Returns:
        The path to the saved audio file.
    """
    tts_client_manager = TTSClient()
    client = tts_client_manager.client
    model_name = tts_client_manager.tts_model_name

    response = client.audio.speech.create(
        model=model_name,
        voice=voice,
        input=text
    )

    # The response content is the audio stream. Save it to a file.
    response.stream_to_file(output_filepath)

    return output_filepath
