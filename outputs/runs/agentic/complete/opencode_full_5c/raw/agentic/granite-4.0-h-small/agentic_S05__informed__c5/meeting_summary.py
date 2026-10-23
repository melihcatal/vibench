import asyncio
from google.cloud import generativeai as genai
from .speech_client import get_google_client
from .speech_models import normalize_google_response, TranscriptEvent

# Summarize live meeting transcript chunks using Gemini LLM.
# Accepts streaming speech events and produces a short meeting summary after each chunk.
# Provider identifiers: Google Cloud Speech, Google Gemini API


async def summarize_meeting(audio_iter=None, temperature=0.2):
    """
    Streams audio, collects transcript events, sends accumulated text to Gemini for summarization.
    Yields a summary string after each chunk.
    """
    client = get_google_client()  # placeholder for actual recognizer usage
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-mini")

    accumulated = ""
    for audio_chunk in audio_iter:
        # Simulated recognition event; replace with actual event handling
        text = "Team discussed project timeline and upcoming milestones"  # placeholder
        accumulated += " " + text
        # Generate summary for current chunk
        response = model.generate_content(
            accumulated, generation_config={"temperature": temperature}
        )
        yield response.text.strip()
