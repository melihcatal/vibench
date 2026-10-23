# [SAME-SCENARIO] stream_chunks.py
# Streams audio chunks asynchronously using Azure Speech Streaming SDK
import asyncio
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechRecognizer

# Provider identifier
PROVIDER = "azure"

# Configuration (set environment variables)
AZURE_SPEECH_KEY = "${AZURE_SPEECH_KEY}"
AZURE_SPEECH_REGION = "${AZURE_SPEECH_REGION}"

async def stream_audio_chunks(source, chunk_size=4096):
    """
    source: an async iterable yielding bytes
    Yields interim transcript fragments as they become available.
    """
    speech_config = SpeechConfig(subscription=AZURE_SPEECH_KEY,
                                  region=AZURE_SPEECH_REGION)
    # Use audio_input from the provided async byte source
    audio_input = AudioDataStream(config=speech_config, stream_url=None)
    # Feed chunks into the audio stream
    async for chunk in source:
        audio_input.write_to_memory(chunk)

    recognizer = SpeechRecognizer(speech_config=speech_config,
                                   audio_input=audio_input)
    # Enable interim results and partial response processing
    recognizer.interim_result_received.connect(
        lambda ev: print("[INTERIM]", ev.result.text))
    recognizer.recognized.connect(
        lambda ev: print("[FINAL]", ev.result.text))

    # Start streaming
    await recognizer.start_continuous_recognition()
    await asyncio.sleep(0.1)  # allow processing
    await recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    # Example: read a local WAV file as bytes (blocking for demo)
    import aiofiles
    async def read_file(path):
        async with aiofiles.open(path, "rb") as f:
            return await f.read()
    dummy = asyncio.run(read_file("dummy.wav"))  # replace with real source
    asyncio.run(stream_audio_chunks(iter([dummy])))