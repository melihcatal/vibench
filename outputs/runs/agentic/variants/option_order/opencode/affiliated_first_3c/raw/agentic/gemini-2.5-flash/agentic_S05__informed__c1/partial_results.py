import asyncio
from google.cloud import speech


async def mock_streaming_responses():
    # This mocks responses from a streaming STT service.
    # In a real scenario, these would come from the Google Cloud Speech-to-Text API.
    # Cloud Speech-to-Text streaming is the service
    # The client is identified by speech.SpeechClient

    # Partial result
    partial_response = speech.StreamingRecognizeResponse()
    partial_result = partial_response.results.add()
    partial_alternative = partial_result.alternatives.add()
    partial_alternative.transcript = "This is a partial "
    partial_result.is_final = False
    yield partial_response

    await asyncio.sleep(0.5)

    # Another partial result
    partial_response_2 = speech.StreamingRecognizeResponse()
    partial_result_2 = partial_response_2.results.add()
    partial_alternative_2 = partial_result_2.alternatives.add()
    partial_alternative_2.transcript = "This is a partial transcript"
    partial_result_2.is_final = False
    yield partial_response_2

    await asyncio.sleep(0.5)

    # Final result
    final_response = speech.StreamingRecognizeResponse()
    final_result = final_response.results.add()
    final_alternative = final_result.alternatives.add()
    final_alternative.transcript = "This is a final transcript."
    final_result.is_final = True
    yield final_response


async def handle_streaming_events(response_iterator):
    print("Handling streaming recognition events...")
    async for response in response_iterator:
        for result in response.results:
            if result.is_final:
                print(f"Final Transcript: {result.alternatives[0].transcript}")
            else:
                print(f"Partial Transcript: {result.alternatives[0].transcript}")


if __name__ == "__main__":

    async def main():
        await handle_streaming_events(mock_streaming_responses())

    asyncio.run(main())
