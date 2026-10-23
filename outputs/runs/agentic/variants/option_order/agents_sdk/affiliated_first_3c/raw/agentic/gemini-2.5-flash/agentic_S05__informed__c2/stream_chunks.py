import asyncio
import os
from google.cloud import speech

# For demonstration, simulate an async audio source
async def async_audio_chunk_generator(audio_file_path: str, chunk_size: int = 4096):
    """Simulates an asynchronous audio chunk source."""
    print(f"Reading audio from {audio_file_path}")
    try:
        with open(audio_file_path, "rb") as audio_file:
            while True:
                chunk = audio_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
                await asyncio.sleep(0.01)  # Simulate async reading/processing delay
    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_file_path}")
        return

async def stream_audio_chunks(audio_source_path: str, language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, # Assuming 16kHz for demonstration audio
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    print("Starting streaming recognition from chunks...")
    audio_chunks = async_audio_chunk_generator(audio_source_path)
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        async for chunk in audio_chunks
    )

    responses = client.streaming_recognize(config=streaming_config, requests=requests)

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            yield f"Final: {transcript}"
        else:
            yield f"Interim: {transcript}"

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
    else:
        # Replace with a path to a test WAV file (16kHz, mono, LINEAR16)
        TEST_AUDIO_FILE = "./test_audio.wav"
        print(f"Make sure you have a 16kHz, mono, LINEAR16 WAV file at {TEST_AUDIO_FILE}")
        print("For example, you can convert an audio file using ffmpeg:")
        print("ffmpeg -i input.mp3 -ar 16000 -ac 1 -c:a pcm_s16le test_audio.wav")
        try:
            asyncio.run(async def_main(TEST_AUDIO_FILE)():
                async for transcript in stream_audio_chunks(TEST_AUDIO_FILE):
                    print(transcript)
            )()
        except Exception as e:
            print(f"An error occurred: {e}")
