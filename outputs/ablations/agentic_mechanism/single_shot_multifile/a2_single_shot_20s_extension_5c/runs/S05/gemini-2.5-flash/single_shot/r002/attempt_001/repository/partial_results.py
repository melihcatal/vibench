import os
import asyncio
import assemblyai as aai

from speech_client import get_assemblyai_realtime_client
from speech_models import TranscriptChunk

async def handle_realtime_transcription(
    audio_data_generator,
    on_partial_result=None,
    on_final_result=None,
    sample_rate=16000
):
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = get_assemblyai_realtime_client()

    async def send_audio():
        async for chunk in audio_data_generator:
            await client.send_audio(chunk)

    async with client as ws_client:
        await ws_client.connect()
        await ws_client.send_session_begins(audio_sample_rate=sample_rate)

        audio_task = asyncio.create_task(send_audio())

        async for msg in ws_client:
            if msg.message_type == aai.RealtimeMessageTypes.PartialTranscript: # Use specific enum
                if on_partial_result and msg.text:
                    chunk = TranscriptChunk(text=msg.text, start_time=msg.audio_start, end_time=msg.audio_end, is_final=False)
                    on_partial_result(chunk)
            elif msg.message_type == aai.RealtimeMessageTypes.FinalTranscript: # Use specific enum
                if on_final_result and msg.text:
                    chunk = TranscriptChunk(text=msg.text, start_time=msg.audio_start, end_time=msg.audio_end, is_final=True)
                    on_final_result(chunk)

        await audio_task
