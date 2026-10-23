import json
import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from websocket import create_connection
import time

# This file demonstrates starting a streaming recognizer with language and punctuation settings
# using IBM Watson Speech to Text.

# IBM Watson Speech to Text service credentials
IBM_WATSON_SPEECH_TO_TEXT_APIKEY = os.environ.get("IBM_WATSON_SPEECH_TO_TEXT_APIKEY")
IBM_WATSON_SPEECH_TO_TEXT_URL = os.environ.get("IBM_WATSON_SPEECH_TO_TEXT_URL")

# Dummy audio source for demonstration
def dummy_audio_stream(chunk_size=1024, sample_rate=16000):
    """Simulates an audio stream yielding chunks."""
    print("Simulating audio stream for IBM Watson...")
    for _ in range(5):
        # Simulate 1 second of silent audio (16kHz, 16-bit mono)
        chunk = b'\x00' * sample_rate * 2
        yield chunk
        time.sleep(1)
    print("Finished simulating audio stream.")

def stream_with_language_settings():
    if not IBM_WATSON_SPEECH_TO_TEXT_APIKEY or not IBM_WATSON_SPEECH_TO_TEXT_URL:
        print("Error: IBM_WATSON_SPEECH_TO_TEXT_APIKEY and IBM_WATSON_SPEECH_TO_TEXT_URL must be set.")
        return

    # Authenticate with IBM Watson
    authenticator = IAMAuthenticator(IBM_WATSON_SPEECH_TO_TEXT_APIKEY)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )
    speech_to_text.set_service_url(IBM_WATSON_SPEECH_TO_TEXT_URL)

    # Generate an access token
    access_token = authenticator.token_manager.get_token()

    # Construct the WebSocket URL for streaming recognition
    # This includes language and punctuation settings
    # Full list of parameters: https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-specify-parameters#specify-parameters-websockets
    websocket_url = (
        IBM_WATSON_SPEECH_TO_TEXT_URL.replace("https://", "wss://") +
        "/v1/recognize?access_token=" + access_token +
        "&model=en-US_BroadbandModel" +
        "&interim_results=true" +
        "&timestamps=true" +
        "&max_alternatives=1" +
        "&smart_formatting=true" + # Enable smart formatting for punctuation
        "&speech_detector_sensitivity=0.5" # Example of another setting
    )

    print(f"Connecting to IBM Watson Speech to Text WebSocket at: {websocket_url}")
    try:
        ws = create_connection(websocket_url)
        print("Connected to IBM Watson. Sending start message...")

        # Send the start message with audio format details
        start_message = {
            "action": "start",
            "content-type": "audio/l16;rate=16000",
            "inactivity_timeout": -1 # Keep connection open indefinitely
        }
        ws.send(json.dumps(start_message))

        # Send audio chunks
        for audio_chunk in dummy_audio_stream():
            ws.send(audio_chunk, opcode=2) # opcode=2 for binary data
            result_json = ws.recv()
            result = json.loads(result_json)

            if "results" in result and result["results"]:
                for r in result["results"]:
                    if r["final"]:
                        yield f"Final: {r["alternatives"][0]["transcript"]}"
                    else:
                        yield f"Partial: {r["alternatives"][0]["transcript"]}"

        # Send the stop message
        print("Finished sending audio. Sending stop message...")
        ws.send(json.dumps({"action": "stop"}))

        # Receive any remaining final results
        while True:
            try:
                result_json = ws.recv()
                result = json.loads(result_json)
                if "results" in result and result["results"]:
                    for r in result["results"]:
                        if r["final"]:
                            yield f"Final: {r["alternatives"][0]["transcript"]}"
            except Exception:
                break # No more messages

        ws.close()
        print("WebSocket connection closed.")

    except Exception as e:
        print(f"Error during IBM Watson streaming: {e}")

if __name__ == "__main__":
    # Set IBM Watson Speech to Text credentials in environment variables:
    # export IBM_WATSON_SPEECH_TO_TEXT_APIKEY="YOUR_API_KEY"
    # export IBM_WATSON_SPEECH_TO_TEXT_URL="YOUR_SERVICE_URL"
    for transcript in stream_with_language_settings():
        print(transcript)
