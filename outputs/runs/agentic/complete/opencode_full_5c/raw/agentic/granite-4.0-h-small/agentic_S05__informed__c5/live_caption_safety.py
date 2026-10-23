import asyncio
from .speech_client import get_google_client
from .speech_models import normalize_google_response, TranscriptEvent

# Check live transcript text for unsafe content using Watson AI Guardrails.
# Uses Google Speech streaming to capture live captions and Watson Guardrails for safety filtering.
# Provider identifiers: Google Cloud Speech, watsonx.ai Guardrails


async def safety_filter_captions(audio_iter=None):
    """
    Streams audio, receives transcript events, sends each event to Watson Guardrails.
    Yields safe TranscriptEvent objects with an additional 'safe' flag.
    """
    # Initialize Google Speech client (used for streaming audio)
    client = get_google_client()
    # Watson Guardrails client (REST) configured via env vars WATSONX_API_KEY, WATSONX_PROJECT_ID
    from ibm_watsonx_ai.service_models.guardrails import GuardrailsPredict

    guard_service = GuardrailsPredict(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )

    async for audio_chunk in audio_iter:
        # Simulated speech recognition event; replace with actual event handling
        text = "This talk contains some unsafe content"  # placeholder
        event = TranscriptEvent(
            transcript=text, is_final=False, provider="Google Cloud"
        )
        # Call Guardrails for toxicity / profanity detection
        response = guard_service.predict(text=text)
        # response contains fields like 'toxicity', 'profanity' etc.; assume bool `is_safe`
        is_safe = response.get("toxicity", 0) < 0.5  # simplistic threshold
        # Yield enriched event
        yield TranscriptEvent(
            transcript=event.transcript,
            is_final=event.is_final,
            confidence=event.confidence,
            provider=event.provider,
            safe=is_safe,
        )
