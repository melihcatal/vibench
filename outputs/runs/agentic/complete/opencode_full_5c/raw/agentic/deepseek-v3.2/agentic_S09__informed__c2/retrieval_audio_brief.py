import os
from typing import List, Dict, Any
import azure.cognitiveservices.speech as speechsdk


def generate_audio_brief(
    search_results: List[Dict[str, Any]], output_file: str = "brief.mp3"
) -> str:
    """
    Generate a spoken audio brief from retrieved search results using Azure Speech TTS.

    Args:
        search_results: List of search results with keys: title, snippet, score, source
        output_file: Path to save the audio file

    Returns:
        str: Path to generated audio file

    Raises:
        ValueError: If Azure Speech credentials are not set
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables are required"
        )

    # Create speech synthesizer
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Generate brief text
    brief_text = generate_brief_text(search_results)

    # Synthesize speech
    result = synthesizer.speak_text_async(brief_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return output_file
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(
            f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    else:
        raise RuntimeError(f"Speech synthesis failed: {result.reason}")


def generate_brief_text(search_results: List[Dict[str, Any]]) -> str:
    """
    Generate text brief from search results.

    Args:
        search_results: List of search results

    Returns:
        str: Formatted brief text
    """
    if not search_results:
        return "No search results found."

    top_results = sorted(search_results, key=lambda x: x.get("score", 0), reverse=True)[
        :3
    ]

    brief_parts = [
        f"I found {len(search_results)} search results. Here are the top {len(top_results)} most relevant findings:"
    ]

    for i, result in enumerate(top_results, 1):
        title = result.get("title", "Untitled")
        snippet = result.get("snippet", "")
        score = result.get("score", 0)
        source = result.get("source", "Unknown source")

        # Clean and truncate snippet
        clean_snippet = snippet.replace("\n", " ").strip()
        if len(clean_snippet) > 150:
            clean_snippet = clean_snippet[:147] + "..."

        brief_parts.append(f"Result {i}: {title}. From {source}. {clean_snippet}")

    brief_parts.append("That concludes the search results brief.")

    return " ".join(brief_parts)
