import os
import azure.cognitiveservices.speech as speechsdk
from speech_models import TranscriptionPayload

# Azure Speech-to-Text API endpoint and key
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-speech-to-text

def transcribe_audio(payload: TranscriptionPayload, config: dict = None):
    api_key = config.get('api_key') or os.environ.get("AZURE_SPEECH_KEY") # Same key as TTS for simplicity
    region = config.get('region') or os.environ.get("AZURE_SPEECH_REGION")

    if not api_key or not region:
        raise ValueError("Azure Speech API key and region must be provided or set as environment variables AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.")

    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

    # Set the target language for transcription
    speech_config.speech_recognition_language = payload.language

    # Create an audio config from the audio bytes
    # For in-memory audio, you typically need to use PushAudioInputStream or PullAudioInputStream
    # For this example, we'll simulate by writing to a temp file and then reading (not ideal for real-time)
    # A more robust solution would involve streaming the bytes directly to the SDK if it supports it for Python's in-memory bytes.
    # Given the constraint of not creating temp files, and the SDK's common usage with file paths or streams,
    # I will adapt to use a PushAudioInputStream which can take bytes.
    audio_config = speechsdk.audio.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
    audio_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Write the audio bytes to the push stream
    # This part requires a bit of manual handling as direct bytes might not be straightforward to push
    # The SDK expects a stream of audio data. Let's use a simple approach for demonstration.
    # In a real scenario, you would manage the PushAudioInputStream directly with the audio source.
    
    # For this example, I'll demonstrate with a simplified approach, assuming the SDK can take bytes for a single shot recognition.
    # However, the SDK is designed for streams or files. Let me re-evaluate the best way to handle 'audio_bytes'.
    # The Speech SDK's `recognize_once_async` usually works with `AudioConfig(filename=...)` or a stream.
    # Since we have `audio_bytes`, we need to feed it to a stream. PushAudioInputStream is appropriate.
    
    # Let's re-implement the audio input for transcription using PushAudioInputStream correctly.
    
    push_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
    audio_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    # Start continuous recognition. This is often used for longer audio. For a single chunk, recognize_once_async is better.
    # However, to feed bytes into a push stream, we need to manage the stream.
    
    # For 'tts_qa_transcript.py', we are expecting a chunk of audio bytes. So recognize_once_async is appropriate.
    # The challenge is feeding the `audio_bytes` into `recognize_once_async` via an `AudioConfig`.
    # The Python SDK doesn't have a direct `AudioConfig.from_bytes`.
    # The recommended way is to use `AudioConfig(stream=audio_input_stream)` where `audio_input_stream` is `PushAudioInputStream`.
    # And then `push_stream.write(audio_bytes)` and `push_stream.close()`.

    push_stream.write(payload.audio_bytes)
    push_stream.close()

    result = audio_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {'transcript': result.text, 'language': payload.language, 'confidence': result.confidence}
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return {'transcript': "", 'language': payload.language, 'confidence': 0.0, 'message': "No speech could be recognized"}
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(f"Speech Recognition canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")

    return {'transcript': "", 'language': payload.language, 'confidence': 0.0, 'message': "Unknown error during transcription"}
