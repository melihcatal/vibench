# [SAME-SCENARIO] stream_microphone.py
import asyncio
import json
import speech_recognition as sr

# Conrete provider: Google Cloud Speech-to-Text Streaming
# This example uses the Google Cloud Speech client library (google-cloud-speech)

# Configure client credentials via environment variable GOOGLE_APPLICATION_CREDENTIALS

async def stream_microphone():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    # Create a gRPC streaming recognition config
    config = {
        "config": {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 16000,
            "language_code": "en-US",
            "enable_automatic_punctuation": True,
        }
    }

    async with sr.Streamer(microphone, 10.0) as stream:
        # Send initial config
        await stream.send(json.dumps(config))
        while True:
            audio = stream.buffer()
            if not audio:
                break
            # Send audio chunk
            await stream.send(audio)

            # Process interim results (partial transcripts)
            for result in recognizer.listen(stream, timeout=1):
                if result.partial:  # Interim result
                    print('Interim:', result.text)
                else:  # Final result
                    print('Final:', result.text)

if __name__ == "__main__":
    asyncio.run(stream_microphone())