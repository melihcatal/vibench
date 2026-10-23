# reviewer_brief_audio.py
# LATER-STEP implementation
# Generate a spoken brief for moderation reviewers using Text-to-Speech

import os
from ibm_watsonx_ai import IbmWatsonXAIClient
from ibm_watsonx_ai.tts import Synthesizer

# Global client initialized once
_client: IbmWatsonXAIClient | None = None


def _init_client() -> None:
    global _client
    if _client is None:
        _client = IbmWatsonXAIClient(output_format="json")


def create_spoken_brief(review_text: str, voice: str = "en-us") -> bytes:
    """Generate an audio file (bytes) of a moderation reviewer brief.

    Returns the raw audio bytes.
    """
    _init_client()  # ensure client is ready
    tts = _client.synthesizer
    audio = tts.synthesize(text=review_text, voice=voice, accept="audio/wav")
    return audio  # binary bytes


# Example usage (not executed)
# brief = create_spoken_brief('Message flagged for hate speech')
# with open('moderation_brief.wav', 'wb') as f:
#     f.write(brief)
