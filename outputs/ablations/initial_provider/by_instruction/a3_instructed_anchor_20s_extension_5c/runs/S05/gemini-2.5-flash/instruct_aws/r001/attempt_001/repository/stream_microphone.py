import asyncio
import pyaudio
import websockets
import json

# AWS Transcribe Streaming endpoint configuration
# Replace with your AWS region and a signed URL for the Transcribe Streaming service
# This example uses a placeholder for the pre-signed URL. In a real application,
# you would generate this URL securely on your backend.
AWS_REGION = "us-east-1"
TRANSCRIBE_VOCABULARY_NAME = "my-custom-vocabulary"  # Optional: Replace with your vocabulary name

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

async def stream_microphone_audio():
    """
    Streams microphone audio to AWS Transcribe Streaming and yields interim transcripts.
    """
    # Placeholder for the actual pre-signed URL, which should be generated server-side.
    # Example: wss://transcribestreaming.<region>.amazonaws.com:8443/stream-transcription-websocket
    # For a real application, you would generate a pre-signed URL with boto3.
    # Example:
    # client = boto3.client("transcribe")
    # presigned_url = client.generate_prescribe_url(...)
    # For demonstration, we'll use a generic endpoint; actual requests will fail without a valid signed URL.
    # In a real scenario, this URL would be dynamic and include authentication.
    transcribe_websocket_url = f"wss://transcribestreaming.{AWS_REGION}.amazonaws.com:8443/stream-transcription-websocket"
    print(f"Connecting to AWS Transcribe Streaming at: {transcribe_websocket_url}")

    async with websockets.connect(
        transcribe_websocket_url,
        extra_headers={"X-Amz-Target": "com.amazonaws.transcribe.Transcribe.StartStreamTranscription"},
        ping_interval=5,
        ping_timeout=20
    ) as websocket:
        print("WebSocket connection established.")

        # Send initial settings message
        start_request = {
            "language_code": "en-US",
            "media_encoding": "pcm",
            "sample_rate": RATE,
            # "vocabulary_name": TRANSCRIBE_VOCABULARY_NAME # Uncomment if using a custom vocabulary
        }
        await websocket.send(json.dumps(start_request))

        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        print("Recording audio... Press Ctrl+C to stop.")
        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                # AWS Transcribe expects audio events wrapped in a JSON message
                audio_event = {
                    "audio_event": {
                        "audio_chunk": list(data)  # Convert bytes to a list of integers for JSON serialization
                    }
                }
                await websocket.send(json.dumps(audio_event))

                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    response = json.loads(message)
                    if "transcript" in response and response["transcript"] and "results" in response["transcript"]:
                        for result in response["transcript"]["results"]:
                            if not result["is_partial"]:
                                yield result["alternatives"][0]["transcript"]
                            else:
                                yield f"[Partial] {result['alternatives'][0]['transcript']}"
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosedOK:
                    print("WebSocket connection closed normally.")
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
        except KeyboardInterrupt:
            print("Stopping recording...")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            await websocket.close()
            print("Audio stream and WebSocket closed.")

if __name__ == "__main__":
    async def main():
        async for transcript in stream_microphone_audio():
            print(f"Transcript: {transcript}")

    asyncio.run(main())
