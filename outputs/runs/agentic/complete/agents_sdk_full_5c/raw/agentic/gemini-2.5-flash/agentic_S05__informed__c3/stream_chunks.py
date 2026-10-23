import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

async def stream_audio_chunks(audio_chunks):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Create a PushAudioInputStream to push the audio chunks
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition_async().get()

    for chunk in audio_chunks:
        stream.write(chunk)
        await asyncio.sleep(0.1) # Simulate async processing
    
    stream.close()
    
    while not done:
        await asyncio.sleep(0.5)
    speech_recognizer.stop_continuous_recognition_async().get()

async def main():
    # Example usage with dummy audio chunks
    # In a real scenario, audio_chunks would come from a live source
    dummy_audio = b"" # Replace with actual audio data
    # For demonstration, create a few chunks
    audio_chunks = [dummy_audio[i:i+1024] for i in range(0, len(dummy_audio), 1024)]
    if not audio_chunks: # Add a placeholder chunk if dummy_audio is empty
        audio_chunks = [b'\x00' * 1024] 

    await stream_audio_chunks(audio_chunks)

if __name__ == "__main__":
    # Ensure AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are set as environment variables
    asyncio.run(main())
