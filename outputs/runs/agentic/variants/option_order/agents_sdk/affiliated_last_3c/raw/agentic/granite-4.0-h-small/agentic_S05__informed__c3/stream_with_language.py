# [SAME-SCENARIO] stream_with_language.py
import asyncio
import speech_recognition as sr

# Conrete provider: Cloud Speech-to-Text streaming (Google)
# Demonstrates setting language_code and enable_automatic_punctuation via SDK client

# Make sure GOOGLE_APPLICATION_CREDENTIALS env variable points to your credentials JSON.

def build_config(language_code="en-US", enable_punctuation=True):
    """Return a recognition config dict with language and punctuation options."""
    return {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 16000,
        "language_code": language_code,
        "enable_automatic_punctuation": enable_punctuation,
        "use_enhanced": False,
    }

async def start_stream_recognition(streamer, config):
    """Send config and begin streaming audio."""
    # Initial config request (specific to Google client library)
    await streamer.send(json.dumps({"config": config}))
    while True:
        audio = streamer.buffer()
        if not audio:
            break
        await streamer.send(audio)
        # Process interim results (Google client library supports iterators)
        for result in sr.wait_for_results(streamer):
            if result.partial:
                print('Interim transcript:', result.text)
            else:
                print('Final transcript:', result.text)

if __name__ == '__main__':
    # Example usage; replace with an actual async microphone streamer implementation
    async def mock_microphone():
        # Placeholder for actual microphone async generator
        pass
    config = build_config(language_code="es-ES", enable_punctuation=True)
    asyncio.run(start_stream_recognition(mock_microphone(), config))