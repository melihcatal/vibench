"""Applies category thresholds to decide whether to allow text using AssemblyAI."""
from typing import Dict
from safety_client import get_assemblyai_client
from safety_models import ThresholdDecision


def check_thresholds_assemblyai(audio_file_url: str, thresholds: Dict[str, float]) -> ThresholdDecision:
    """
    Transcribes audio, gets content safety labels from AssemblyAI, and
    applies custom thresholds to make an allow/block decision.

    Args:
        audio_file_url: URL to the audio file to process.
        thresholds: A dictionary of category names to float score thresholds.
                    Example: {'hate_speech': 0.8, 'violence': 0.9}

    Returns:
        A decision object indicating if the content is allowed and why.
    """
    aai = get_assemblyai_client()
    
    config = aai.TranscriptionConfig(content_safety=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_url, config)

    if not transcript.content_safety_labels:
        return ThresholdDecision(allow=True, reasons=[])

    reasons_for_block = []
    safety_summary = transcript.content_safety_labels.summary

    for category, threshold in thresholds.items():
        if category in safety_summary and safety_summary[category] >= threshold:
            reasons_for_block.append(
                f"Blocked due to '{category}' score ({safety_summary[category]:.2f}) "
                f"exceeding threshold ({threshold:.2f})"
            )
            
    allow = not bool(reasons_for_block)
    
    return ThresholdDecision(allow=allow, reasons=reasons_for_block)
