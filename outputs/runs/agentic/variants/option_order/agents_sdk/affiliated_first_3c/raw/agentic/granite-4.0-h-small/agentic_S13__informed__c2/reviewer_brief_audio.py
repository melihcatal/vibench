# [LATER-STEP] reviewer_brief_audio.py

from text_to_speech_client import TextToSpeechClient
from safety_models import TextModerationResult, UnsafeSpan

TTS = TextToSpeechClient()

def generate_reviewer_brief(result: TextModerationResult, spans: List[UnsafeSpan]) -> bytes:
    """Produce a short spoken audio brief summarizing the moderation decision.
    Uses the configured TTS provider.
    Returns raw audio bytes (e.g., WAV or MP3).\n    """
    sections = []\n    sections.append(f\"Mod result: {result.decision}\")\n    for cat, score in result.detailed.items():\n        if score > result.thresholds.get(cat, 0.5):\n            sections.append(f\"Category {cat} score {score}\")\n    for span in spans:\n        sections.append(f\"Flagged {span.category} from {span.start} to {span.end} (score {span.score})\")\n    brief_text = ' '.join(sections)\n    audio = TTS.synthesize(text=brief_text, voice='en-us-female')\n    return audio
