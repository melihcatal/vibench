import asyncio
import assemblyai as aai
from speech_client import get_speech_client

def on_data(transcript: aai.RealtimeTranscript):
    if transcript.text:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print(f"An error occurred: {error}")

async def stream_with_specific_settings():
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    transcriber = get_speech_client()

    # Configure transcription settings
    transcription_config = aai.TranscriptionConfig(
        language_code="es",  # Set language to Spanish
        punctuate=True,      # Enable automatic punctuation
    )

    print("Iniciando transcripción en español con puntuación...")
    
    streamer = transcriber.stream_from_microphone(
        transcription_config=transcription_config,
        on_data=on_data,
        on_error=on_error,
    )

    await streamer.transcribe_async()

if __name__ == "__main__":
    # To run this example:
    # asyncio.run(stream_with_specific_settings())
    print("This script demonstrates streaming with language and punctuation settings using AssemblyAI.")
