# Generate a spoken brief from retrieved search results
import os
import openai

def generate_audio_brief(retrieved_docs: list[tuple[str, float]]) -> str:
    """Create a concise textual brief that can be turned into speech."""
    summary = 'Search results summary: '
    for i, (doc, score) in enumerate(retrieved_docs[:5]):  # top 5 results
        summary += f'#{i+1} score {score:.2f}: {doc} '
    return summary

# Optional: send to TTS provider, e.g., Azure Cognitive Services Speech Service
# tts_client = openai.Audio.synthesize(speech_configuration, text=brief)
