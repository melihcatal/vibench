import os
import websockets
import json

# Use Amazon Transcribe Streaming (AWS SDK boto3)
# Credentials: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


async def start_streaming_recognizer(
    language="en-US", enable_automatic_punctuation=True
):
    """
    Initiates a WebSocket connection to Amazon Transcribe Streaming.
    language: BCP-47 language code (default English)
    enable_automatic_punctuation: bool
    """
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = "us-east-1"
    endpoint = f"wss://{region}.transcribe.amazonaws.com"
    headers = {
        "x-amz-code": "TranscribeStreaming",
        "x-amz-code-version": "v2",
    }
    uri = f"{endpoint}/stream-transcription-websocket"
    auth_params = {
        "credentials": {"accessKeyId": access_key, "secretAccessKey": secret_key},
        "languageCode": language,
        "mediaEncoding": "pcm",
        "punctuationEnabled": enable_automatic_punctuation,
    }

    async with websockets.connect(uri, extra_headers=headers) as ws:
        # Send Initiation
        init_msg = {"action": "start", "format": "audio/l16; rate=16000", **auth_params}
        await ws.send(json.dumps(init_msg))
        print(f"Started streaming recognizer for language {language}")

        try:
            while True:
                audio_chunk = b"..."  # Replace with actual captured audio bytes
                if not audio_chunk:
                    break
                await ws.send(audio_chunk)
                resp = await ws.recv()
                data = json.loads(resp)
                if "interimResults" in data:
                    for result in data["interimResults"]:
                        alt = result.get("alternatives", [{}])[0]
                        print("Interim:", alt.get("transcript", ""))
        except websockets.ConnectionClosed:
            print("Transcribe stream ended")


if __name__ == "__main__":
    asyncio.run(start_streaming_recognizer())
