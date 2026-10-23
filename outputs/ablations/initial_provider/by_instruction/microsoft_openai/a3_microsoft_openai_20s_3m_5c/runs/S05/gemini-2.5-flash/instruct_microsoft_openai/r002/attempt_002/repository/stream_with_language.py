import asyncio
from speech_client import SpeechClient
from speech_models import AudioChunk, RecognitionConfig, RecognitionLanguage

async def async_audio_chunk_source_with_language():
    """Simulates an asynchronous source yielding audio chunks for language streaming."""
    chunk_id = 0
    phrases = [
        "Ceci est un test en français.",
        "Y esto es una prueba en español.",
        "And this is a test in English."
    ]

    for phrase in phrases:
        await asyncio.sleep(0.7)
        # For simulation, encode the phrase as the audio content
        chunk_data = phrase.encode()
        yield AudioChunk(chunk_id=chunk_id, content=chunk_data, sequence_number=chunk_id)
        chunk_id += 1
    yield AudioChunk(chunk_id=chunk_id, content=b"", sequence_number=chunk_id, is_last_chunk=True)

async def stream_recognizer_with_settings(language: RecognitionLanguage, enable_punctuation: bool = True):
    speech_client = SpeechClient()
    # Note: OpenAI Whisper API handles punctuation automatically and does not have a direct enable_automatic_punctuation setting to toggle.
    # The profanity_filter is also not a direct parameter in the OpenAI Whisper API.
    # These are kept for API compatibility with the abstract RecognitionConfig.
    config = RecognitionConfig(
        language=language,
        enable_automatic_punctuation=enable_punctuation, 
        profanity_filter=False # OpenAI Whisper API does not directly expose this option
    )

    print(f"Starting streaming recognizer with language: {language.name} and punctuation: {enable_punctuation}...")
    async for audio_chunk in async_audio_chunk_source_with_language():
        if audio_chunk.is_last_chunk:
            print("End of language streaming.")
            break
        
        print(f"Processing audio chunk {audio_chunk.chunk_id} for language {language.name}")
        transcript_response = await speech_client.stream_audio_for_transcription(audio_chunk, config)
        if transcript_response.text:
            print(f"Recognized Text ({transcript_response.language}): {transcript_response.text}")

async def main():
    print("\n--- Streaming with English ---")
    await stream_recognizer_with_settings(RecognitionLanguage.ENGLISH)

    print("\n--- Streaming with Spanish ---")
    await stream_recognizer_with_settings(RecognitionLanguage.SPANISH, enable_punctuation=False) # Demonstrate setting but note Whisper behavior

    print("\n--- Streaming with French ---")
    await stream_recognizer_with_settings(RecognitionLanguage.FRENCH)

if __name__ == "__main__":
    asyncio.run(main())
