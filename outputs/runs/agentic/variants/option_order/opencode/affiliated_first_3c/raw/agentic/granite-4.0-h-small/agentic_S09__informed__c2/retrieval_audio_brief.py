# retrieval_audio_brief.py
# [LATER-STEP] Generate a spoken brief from retrieved search results

import os
from embeddings_client import get_watsonx_client
from ibm_watsonx_ai.services import TextToSpeech

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

tts_client = TextToSpeech(client=get_watsonx_client())


def generate_audio_brief(result_snippets: list[str]) -> bytes:
    """Create a short spoken audio brief from result snippets."""
    # Combine snippets into a brief script
    script = "\n".join(result_snippets[:5])  # limit to first few for brevity
    # Call Text-to-Speech API to synthesize audio
    audio = tts_client.synthesize(
        text=script, accept="audio/wav", voice="en-US_MichaelV3Voice"
    )
    return audio  # returns binary WAV data
