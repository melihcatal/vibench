# [LATER-STEP] live_caption_safety.py
import asyncio

import speech_client as sc

# Provider: watsonx.ai Guardrails / HAP detection (provider identified via WATSONX_API_KEY usage in helper)

async def live_safety_check(source_iterable):
    """
    Stream audio, generate live captions, and run each caption through the watsonx guardrails detector.
    
    Args:
        source_iterable: async generator yielding raw PCM audio bytes.
    """
    async for result in sc.recognize_streaming(source_iterable):
        if not result.is_partial:
            caption = result.alternatives[0].transcript
            # Provider-specific safety call (REST under the hood)
            safe = await check_content_safety_watsonx(caption)
            if safe:
                print(f"[SAFE] {caption} (clean)")
            else:
                print(f"[FILTERED] {caption} (unsafe)")
                # downstream action: drop or flag this caption
        else:
            # Interim captions can also be screened if needed
            pass

async def check_content_safety_watsonx(text: str) -> bool:
    """Call watsonx guardrails endpoint to assess toxicity or hate speech."""
    from ibm_watsonx_ai import WatsonXApi
    from ibm_watsonx_ai.consts import GuardrailsLevel
    # Provider identification via the api_key usage
    api = WatsonXApi(api_key="", endpoint="https://api.us-south.watsonx.ibm.com/api")
    response = api.detect_guardrails(text, level=GuardrailsLevel.HAP)
    # response returns a dict; safety flag typically under 'safe'
    return response.get('safe', False)

# Example minimal driver (mute):
# async def demo():
#     async for r in live_safety_check(sc.microphone_generator()):
#         pass
