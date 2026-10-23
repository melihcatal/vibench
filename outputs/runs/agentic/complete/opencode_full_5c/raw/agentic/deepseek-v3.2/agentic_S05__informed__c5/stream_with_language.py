import asyncio
from speech_client import get_speech_client


async def start_streaming_recognizer(
    language="en-US",
    enable_punctuation=True,
    enable_word_timestamps=True,
    profanity_filter="masked",
):
    """Start a streaming recognizer with language and punctuation settings."""
    client = get_speech_client()

    # Configure Azure Speech recognizer
    speech_config = client.speech.SpeechConfig(
        subscription=client.speech_key, region=client.speech_region
    )

    # Set language
    speech_config.speech_recognition_language = language

    # Enable dictation for better punctuation
    speech_config.enable_dictation()

    # Request word-level timestamps if enabled
    if enable_word_timestamps:
        speech_config.request_word_level_timestamps()

    # Configure punctuation
    if enable_punctuation:
        speech_config.set_property(
            client.speech.PropertyId.SpeechServiceResponse_RequestPunctuation, "true"
        )

    # Configure profanity filter
    if profanity_filter:
        speech_config.set_property(
            client.speech.PropertyId.SpeechServiceResponse_ProfanityOption,
            profanity_filter,
        )

    # Create push stream for audio input
    push_stream = client.audio.PushAudioInputStream()
    audio_config = client.audio.AudioConfig(stream=push_stream)

    # Create recognizer
    recognizer = client.speech.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print(f"Starting streaming recognizer with language: {language}")
    print(f"Punctuation enabled: {enable_punctuation}")
    print(f"Word timestamps enabled: {enable_word_timestamps}")
    print(f"Profanity filter: {profanity_filter}")

    # Event for completion
    done = asyncio.Event()
    transcripts = []

    def recognized_callback(evt):
        if evt.result.reason == client.speech.ResultReason.RecognizedSpeech:
            transcript = evt.result.text
            print(f"Transcript: {transcript}")
            transcripts.append(transcript)

            # If word timestamps are available, print them
            if hasattr(evt.result, "words") and evt.result.words:
                for word in evt.result.words:
                    print(
                        f"  Word: {word.word} (Offset: {word.offset}, Duration: {word.duration})"
                    )

    def session_stopped_callback(evt):
        print("Session stopped.")
        done.set()

    recognizer.recognized.connect(recognized_callback)
    recognizer.session_stopped.connect(session_stopped_callback)

    # Start continuous recognition
    recognizer.start_continuous_recognition()

    return {
        "recognizer": recognizer,
        "push_stream": push_stream,
        "done_event": done,
        "transcripts": transcripts,
    }


async def stream_audio_to_recognizer(recognizer_info, audio_chunks):
    """Stream audio chunks to an active recognizer."""
    push_stream = recognizer_info["push_stream"]
    done_event = recognizer_info["done_event"]

    try:
        # Feed audio chunks to the stream
        for chunk in audio_chunks:
            if chunk:
                push_stream.write(chunk)
            await asyncio.sleep(0.01)

        # Close the stream to signal end
        push_stream.close()

        # Wait for recognition to complete
        await done_event.wait()

    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        recognizer_info["recognizer"].stop_continuous_recognition()

    return recognizer_info["transcripts"]


async def test_multiple_languages():
    """Test streaming with different language settings."""

    # Test English with punctuation
    print("\n=== Testing English with punctuation ===")
    english_recognizer = await start_streaming_recognizer(
        language="en-US", enable_punctuation=True, enable_word_timestamps=True
    )

    # Mock audio chunks for English
    english_chunks = [b"english_audio_chunk_" + str(i).encode() for i in range(5)]
    english_results = await stream_audio_to_recognizer(
        english_recognizer, english_chunks
    )
    print(f"English results: {english_results}")

    # Test Spanish
    print("\n=== Testing Spanish ===")
    spanish_recognizer = await start_streaming_recognizer(
        language="es-ES", enable_punctuation=True, enable_word_timestamps=False
    )

    # Mock audio chunks for Spanish
    spanish_chunks = [b"spanish_audio_chunk_" + str(i).encode() for i in range(5)]
    spanish_results = await stream_audio_to_recognizer(
        spanish_recognizer, spanish_chunks
    )
    print(f"Spanish results: {spanish_results}")

    # Test French with profanity filtering
    print("\n=== Testing French with profanity filtering ===")
    french_recognizer = await start_streaming_recognizer(
        language="fr-FR", enable_punctuation=True, profanity_filter="masked"
    )

    # Mock audio chunks for French
    french_chunks = [b"french_audio_chunk_" + str(i).encode() for i in range(5)]
    french_results = await stream_audio_to_recognizer(french_recognizer, french_chunks)
    print(f"French results: {french_results}")


if __name__ == "__main__":
    asyncio.run(test_multiple_languages())
