# DashScope Real-time ASR (service=DashScope real-time speech recognition; sdk=dashscope)
# DASHSCOPE_API_KEY environment variable required

import os
import dashscope
import asyncio


async def handle_stream():
    client = dashscope.speech.SpeechRecognition()
    client.api_key = os.getenv("DASHSCOPE_API_KEY")
    # Start streaming recognizer (WebSocket)
    async with client.recognize_stream(language="en-US") as stream:
        async for event in stream:
            if event.type == "partial":
                # Interim partial result
                print("Partial:", event.result.text)
            elif event.type == "final":
                # Final recognition result
                print("Final:", event.result.text)
            else:
                print("Other event:", event.type)


asyncio.run(handle_stream())
