import asyncio
from speech_client import get_speech_client


async def stream_audio_chunks(audio_source):
    """Stream audio chunks from an async source."""
    client = get_speech_client()

    # Configure streaming recognition for Azure Speech
    speech_config = client.speech.SpeechConfig(
        subscription=client.speech_key, region=client.speech_region
    )
    speech_config.speech_recognition_language = "en-US"
    speech_config.enable_dictation()
    speech_config.request_word_level_timestamps()

    # Create push stream for audio chunks
    push_stream = client.audio.PushAudioInputStream()
    audio_config = client.audio.AudioConfig(stream=push_stream)

    # Create recognizer
    recognizer = client.speech.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Starting audio chunk streaming...")

    # Event for completion
    done = asyncio.Event()
    results = []

    def recognized_callback(evt):
        if evt.result.reason == client.speech.ResultReason.RecognizedSpeech:
            transcript = evt.result.text
            print(f"Chunk recognized: {transcript}")
            results.append(transcript)
            yield transcript
        elif evt.result.reason == client.speech.ResultReason.NoMatch:
            print("No match in this chunk")

    def session_stopped_callback(evt):
        print("Session stopped.")
        done.set()

    recognizer.recognized.connect(recognized_callback)
    recognizer.session_stopped.connect(session_stopped_callback)

    # Start continuous recognition
    recognizer.start_continuous_recognition()

    try:
        # Stream audio chunks from the async source
        async for chunk in audio_source:
            if chunk:
                push_stream.write(chunk)
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming

        # Signal end of stream
        push_stream.close()

        # Wait for recognition to complete
        await done.wait()

    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        recognizer.stop_continuous_recognition()

    return results


async def mock_audio_source():
    """Mock async audio source for testing."""
    # In a real implementation, this would yield actual audio chunks
    for i in range(10):
        # Simulate audio chunks (in reality these would be bytes)
        yield b"fake_audio_chunk_" + str(i).encode()
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    # Test with mock audio source
    results = asyncio.run(stream_audio_chunks(mock_audio_source()))
    print(f"Final results: {results}")
