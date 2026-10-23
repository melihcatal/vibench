# Generate spoken briefs for moderation reviewers using ElevenLabs Text to Speech

import os
from typing import Dict
from elevenlabs import generate, set_api_key
from safety_models import SafetyDecision


def generate_reviewer_brief(decisions: Dict[str, List[SafetyDecision]]) -> bytes:
    """Generate spoken briefs for moderation reviewers using ElevenLabs."""
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    
    brief_lines = []
    for text, decision_list in decisions.items():
        flagged = [d["category"] for d in decision_list if d["flagged"]]
        if flagged:
            brief_lines.append(f"Content flagged for: {', '.join(flagged)}.")
        else:
            brief_lines.append("Content allowed.")
    
    brief_text = "Moderation brief: " + " ".join(brief_lines)
    audio = generate(text=brief_text, voice="Rachel", model="eleven_multilingual_v2")
    return audio