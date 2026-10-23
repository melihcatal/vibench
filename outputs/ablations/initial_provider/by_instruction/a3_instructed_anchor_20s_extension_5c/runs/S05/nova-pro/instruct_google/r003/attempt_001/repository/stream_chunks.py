import asyncio
import speech_client

async def stream_chunks(chunks):
    client = speech_client.get_speech_client()
    config = speech_client.create_streaming_config()
    streaming_requests = [speech.types.StreamingRecognizeRequest(streaming_config=config)]
    for chunk in chunks:
        streaming_requests.append(speech.types.StreamingRecognizeRequest(audio_content=chunk))
        if len(streaming_requests) > 1:
            responses = client.streaming_recognize(streaming_requests)
            for response in responses:
                for result in response.results:
                    if not result.alternatives:
                        continue
                    transcript = result.alternatives[0].transcript
                    is_final = result.is_final
                    yield transcript, is_final
            streaming_requests = [speech.types.StreamingRecognizeRequest(streaming_config=config)]