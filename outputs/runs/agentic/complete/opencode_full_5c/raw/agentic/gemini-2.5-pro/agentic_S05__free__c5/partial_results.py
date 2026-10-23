import asyncio
from google.cloud import speech
from speech_client import get_speech_client, get_streaming_config


async def handle_partial_and_final_results(audio_chunk_generator):
    client = get_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=get_streaming_config(),
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunk_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config, request_generator())

    final_transcripts = []
    interim_transcript = ""

    async for response in responses:
        for result in response.results:
            transcript = result.alternatives[0].transcript
            if result.is_final:
                final_transcripts.append(transcript)
                interim_transcript = ""
                yield {"final_transcript": transcript, "is_final": True}
            else:
                interim_transcript = transcript
                yield {"interim_transcript": interim_transcript, "is_final": False}
