# [LATER-STEP] meeting_summary.py
import asyncio

import speech_client as sc
from speech_models import StreamingRecognitionResult, normalize_provider_result

# Provider: Gemini API (text chat) for meeting summarization (provider identified via GOOGLE_API_KEY usage)

async def meeting_summary(source_iterable, model="gemini-1.5-flash"):
    """
    Stream live audio, transcribe to text, and send each finalized transcript chunk
    to the Gemini model for incremental meeting summary generation.
    
    Args:
        source_iterable: async generator yielding raw PCM audio bytes.
        model: Gemini model identifier (provider-specific).
    """
    async for result in sc.recognize_streaming(source_iterable):
        if not result.is_partial:
            # Normalize provider-specific result into our local object for consistent usage
            cap = normalize_provider_result(result)
            final_text = cap.alternatives[0].transcript
            summary = await summarize_with_gemini(final_text, model=model)
            print(f"[SUMMARY] {summary}")
        else:
            # Optionally feed interim chunks to the model for ongoing summarization
            pass

async def summarize_with_gemini(text: str, model: str = "gemini-1.5-flash") -> str:
    """Call the Gemini API (provider SDK) to produce a meeting summary."""
    from google.generativeai import GenerationModel
    # Provider identification via the model name and credentials (GOOGLE_API_KEY env var)
    gemini = GenerationModel(model)
    response = await gemini.generate_content(text, generation_config={"temperature": 0.3})
    # Gemini returns a GenerationResponse with .text attribute
    return response.text.strip()

# Example driver (mute):
# async def mic():
#     for chunk in sc.microphone_generator():
#         yield chunk
# async for s in meeting_summary(mic()):
#     pass
