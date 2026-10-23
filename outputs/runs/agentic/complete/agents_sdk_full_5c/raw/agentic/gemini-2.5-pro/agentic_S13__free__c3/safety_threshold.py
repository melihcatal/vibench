import os
from typing import Dict, List

import assemblyai

from safety_client import get_assemblyai_client
from safety_models import ModerationResponse, SafetyDecision, SafetyCategory


def apply_safety_thresholds(
    text: str, thresholds: Dict[str, float]
) -> ModerationResponse:
    """
    Applies custom thresholds to content safety categories from AssemblyAI.
    """
    client = get_assemblyai_client()
    if not client:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=text,
                    is_safe=False,
                    reason="AssemblyAI client not configured.",
                    categories=[],
                )
            ]
        )

    config = assemblyai.TranscriptionConfig(content_safety=True)

    try:
        # AssemblyAI's primary interface is for audio, but we can pass text directly
        # to the content safety models. This is a conceptual adaptation.
        # The SDK requires a file, so we simulate a dummy use case.
        # A more direct text method would be via their raw API if available.
        transcript = client.transcribe_string(text, config)

        if not transcript.content_safety_labels:
             return ModerationResponse(decisions=[SafetyDecision(text=text, is_safe=True)])

        flagged_categories = []
        is_safe = True
        
        # In a real scenario, you'd check transcript.content_safety.results
        # This is a mock structure based on SDK docs.
        results = transcript.content_safety_labels.results
        
        for result in results:
            label = result.label
            confidence = result.confidence
            threshold = thresholds.get(label, 0.99) # Default to high threshold

            if confidence >= threshold:
                is_safe = False
                flagged_categories.append(
                    SafetyCategory(
                        category=label,
                        score=confidence,
                        threshold=threshold,
                    )
                )

        reason = (
            ", ".join(c.category for c in flagged_categories)
            if not is_safe
            else "Safe"
        )
        decision = SafetyDecision(
            text=text, is_safe=is_safe, reason=reason, categories=flagged_categories
        )

        return ModerationResponse(decisions=[decision])

    except Exception as e:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=text,
                    is_safe=False,
                    reason=f"API Error: {e}",
                    categories=[],
                )
            ]
        )
