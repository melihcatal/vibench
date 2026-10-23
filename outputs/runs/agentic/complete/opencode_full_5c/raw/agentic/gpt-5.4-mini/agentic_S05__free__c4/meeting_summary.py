from openai import OpenAI
from speech_client import load_config
from speech_models import join_chunks, TranscriptChunk

async def meeting_summary(chunks: list[TranscriptChunk]) -> str:
    client = OpenAI(api_key=load_config().openai_api_key)
    transcript = join_chunks(chunks)
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize this meeting transcript concisely: {transcript}",
    )
    return resp.output_text
