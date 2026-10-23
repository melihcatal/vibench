from google.cloud import speech
import asyncio

async def process_speech_recognition_events(responses_async_iterator):
    """
    Processes an async iterator of Google Cloud Speech-to-Text responses,
    handling partial and final transcripts.
    Args:
        responses_async_iterator: An async iterator yielding SpeechRecognizeResponse objects.
    """
    print("Processing speech recognition events...")
    async for response in responses_async_iterator:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                yield {"type": "final", "transcript": transcript, "confidence": result.alternatives[0].confidence}
            else:
                yield {"type": "partial", "transcript": transcript}

if __name__ == "__main__":
    # Mock function to simulate an async iterator of responses from Google Cloud Speech-to-Text
    async def mock_responses_iterator():
        # Simulate a partial result
        partial_response = speech.StreamingRecognizeResponse()
        partial_result = speech.StreamingRecognitionResult()
        partial_alternative = speech.SpeechRecognitionAlternative(transcript="hello there", confidence=0.0)
        partial_result.alternatives.append(partial_alternative)
        partial_result.is_final = False
        partial_response.results.append(partial_result)
        yield partial_response
        await asyncio.sleep(0.5)

        # Simulate a final result
        final_response = speech.StreamingRecognizeResponse()
        final_result = speech.StreamingRecognitionResult()
        final_alternative = speech.SpeechRecognitionAlternative(transcript="hello there how are you", confidence=0.95)
        final_result.alternatives.append(final_alternative)
        final_result.is_final = True
        final_response.results.append(final_result)
        yield final_response
        await asyncio.sleep(0.5)

        # Simulate another partial result
        partial_response_2 = speech.StreamingRecognizeResponse()
        partial_result_2 = speech.StreamingRecognitionResult()
        partial_alternative_2 = speech.SpeechRecognitionAlternative(transcript="I am doing", confidence=0.0)
        partial_result_2.alternatives.append(partial_alternative_2)
        partial_result_2.is_final = False
        partial_response_2.results.append(partial_result_2)
        yield partial_response_2
        await asyncio.sleep(0.5)

        # Simulate another final result
        final_response_2 = speech.StreamingRecognizeResponse()
        final_result_2 = speech.StreamingRecognitionResult()
        final_alternative_2 = speech.SpeechRecognitionAlternative(transcript="I am doing great thank you", confidence=0.98)
        final_result_2.alternatives.append(final_alternative_2)
        final_result_2.is_final = True
        final_response_2.results.append(final_result_2)
        yield final_response_2

    async def main():
        print("Starting to process mock responses...")
        async for event in process_speech_recognition_events(mock_responses_iterator()):
            if event["type"] == "partial":
                print(f"Partial Transcript: {event["transcript"]}")
            elif event["type"] == "final":
                print(f"Final Transcript: {event["transcript"]} (Confidence: {event["confidence"]:.2f})")

    asyncio.run(main())
